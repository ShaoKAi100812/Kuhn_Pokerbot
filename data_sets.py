# <ASSIGNMENT: Generate and load your data sets. Motivate your choices in the docstrings and comments. This file
# contains a suggested structure; you are free to define your own structure, adjust function arguments etc. Don't forget
# to write appropriate tests for your functionality.>

import os
import random
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from skimage import filters

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Current file marks the root directory
TRAINING_IMAGE_DIR = os.path.join(ROOT_DIR, "data_sets", "training_images")  # Directory for storing training images (targt address)
TEST_IMAGE_DIR = os.path.join(ROOT_DIR, "data_sets", "test_images")  # Directory for storing test images (targt address)
FEATURE_IMAGE_DIR = os.path.join(ROOT_DIR, "data_sets", "feature_images")  # Directory for storing feature images (targt address)
MODEL_DIR = os.path.join(ROOT_DIR, "model_sets")        # Directory for storing model parameters
LABELS = ['J', 'Q', 'K', 'A']  # Possible card labels
IMAGE_SIZE = 32 
ROTATE_MAX_ANGLE = 180

FONTS = [
    font_manager.findfont(font_manager.FontProperties(family = 'sans-serif', style = 'normal', weight = 'normal')),
    font_manager.findfont(font_manager.FontProperties(family = 'sans-serif', style = 'italic', weight = 'normal')),
    font_manager.findfont(font_manager.FontProperties(family = 'sans-serif', style = 'normal', weight = 'medium')),
    font_manager.findfont(font_manager.FontProperties(family = 'serif', style = 'normal', weight = 'normal')),
    font_manager.findfont(font_manager.FontProperties(family = 'serif', style = 'italic', weight = 'normal')),
    font_manager.findfont(font_manager.FontProperties(family = 'serif', style = 'normal', weight = 'medium')),
]  # True type system fonts


def extract_features(img: Image, file_name = None):   # input one image object
    """
    Convert an image to features that serve as input to the image classifier.

    Arguments
    ---------
    img : Image
        Image to convert to features.
    file_name : str, default = None
        Passing the file name to save_without_generate() to save the feature image for easy observation.

    Returns
    -------
    features : list/matrix/structure of int, int between zero and one
        Extracted features in a format that can be used in the image classifier.
    """
    # <ASSIGNMENT: Implement your feature extraction by converting pixel intensities to features.>
    
    # step 1: Apply light Gaussian blur 
    im = img.filter(ImageFilter.GaussianBlur(0.5))
    
    # step 2: Apply single value threshold
    pixels = list(im.getdata())
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if pixels[i*im.size[1]+j] <= 175:     # bigger threshold for keeping more info
                pixels[i*im.size[1]+j] = 0
            else:
                pixels[i*im.size[1]+j] = 255
    im.putdata(pixels)
    
    # step 3: Apply 3*3 averaging blur
    im = im.filter(ImageFilter.Kernel((3,3),(1,1,1,1,1,1,1,1,1)))
    
    # step 4: Apply hysteresis threshold
    pixels = list(im.getdata())
    pixels = np.array(pixels)
    # inverse pixel value for filters
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixels[i*im.size[1]+j] = 255 - pixels[i*im.size[1]+j]
    pixels = list(filters.apply_hysteresis_threshold(pixels, 125, 175).astype(int))
    # filter the most external noises out because of not overlapping
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if i <= 1 or i >= im.size[0]-2 or j <= 1 or j >= im.size[1]-2: 
                pixels[i*im.size[1]+j] = 0
    features = np.array(pixels)
    features = np.reshape(features, (IMAGE_SIZE, IMAGE_SIZE, 1))
    
    # step 5: saving feature images to directory for observation
    if not file_name==None:                           # only execuate when the filename is given
        for i in range(im.size[0]):
            for j in range(im.size[1]):
                if pixels[i*im.size[1]+j] == 1:
                    pixels[i*im.size[1]+j] = 0        # 0 for image storage
                else:
                    pixels[i*im.size[1]+j] = 255      # 255 for image storage
        im.putdata(pixels)
        save_without_generate(im, file_name, FEATURE_IMAGE_DIR)
    
    return features


def load_data_set(data_dir, n_validation = 0):
    """
    Prepare features for the images in data_dir and divide in a training and validation set.

    Parameters
    ----------
    data_dir : str
        Directory of images to load
    n_validation : int, default = 0
        Number of images that are assigned to the validation set
    """

    # Extract png files
    files = os.listdir(data_dir)
    png_files = []
    for file in files:
        if file.split('.')[-1] == "png":
            png_files.append(file)
            
    random.shuffle(png_files) # Shuffled list of the png-file names that are stored in data_dir

    # <ASSIGNMENT: Load the training and validation set and prepare the features and labels. Use extract_features()
    # to convert a loaded image (you can load an image with Image.open()) to features that can be processed by your
    # image classifier. You can extract the original label from the image filename.>
    
    # initialize features and labels
    training_features = []
    training_labels = []
    validation_features = []
    validation_labels = []
    counter = 0
    dummy_num = []
    for png_file in png_files:
        # tranform str to dummy variables
        if png_file[0] == 'J':
            dummy_num = [1, 0, 0, 0]
        elif png_file[0] == 'Q':
            dummy_num = [0, 1, 0, 0]
        elif png_file[0] == 'K':
            dummy_num = [0, 0, 1, 0]
        elif png_file[0] == 'A':
            dummy_num = [0, 0, 0, 1]
        else:
            raise ValueError("No this label!")

        if counter < len(png_files)-n_validation:
            # assign features one by one using extract_features()
            training_features.append(extract_features(Image.open(f"{data_dir}\\{png_file}"), png_file))
            # assign labels by extracting from image filenames
            training_labels.append(dummy_num)
        else:
            # assign features one by one using extract_features()
            validation_features.append(extract_features(Image.open(f"{data_dir}\\{png_file}"), png_file))
            # assign labels by extracting from image filenames
            validation_labels.append(dummy_num)
        counter += 1

    return np.array(training_features), np.array(training_labels), np.array(validation_features), np.array(validation_labels)


def generate_data_set(n_samples, data_dir):
    """
    Generate n_samples noisy images by using generate_noisy_image(), and store them in data_dir.

    Arguments
    ---------
    n_samples : int
        Number of train/test examples to generate
    data_dir : str in [TRAINING_IMAGE_DIR, TEST_IMAGE_DIR]
        Directory for storing images
    """

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)  # Generate a directory for data set storage, if not already present

    for i in range(n_samples):
        # <ASSIGNMENT: Replace with your implementation. Pick a random rank and convert it to a noisy image through
        # the generate_noisy_image() function below.>
        rank = random.choice(LABELS)
        noise = random.uniform(0, 0.7)           # define training/testing noise level
        img = generate_noisy_image(rank, noise)

        img.save(f"{data_dir}\\{rank}_{i}.png")  # The filename encodes the original label for training/testing


def generate_noisy_image(rank, noise_level):
    """
    Generate a noisy image with a given noise corruption. This implementation mirrors how the server generates the
    images. However the exact server settings for noise_level and ROTATE_MAX_ANGLE are unknown.
    For the PokerBot assignment you won't need to update this function, but remember to test it.

    Arguments
    ---------
    rank : str in ['J', 'Q', 'K', 'A']
        Original card rank.
    noise_level : int between zero and one
        Probability with which a given pixel is randomized.

    Returns
    -------
    noisy_img : Image
        A noisy image representation of the card rank.
    """

    if not 0 <= noise_level <= 1:
        raise ValueError(f"Invalid noise level: {noise_level}, value must be between zero and one")
    if rank not in LABELS:
        raise ValueError(f"Invalid card rank: {rank}")

    # Create rank image from text
    font = ImageFont.truetype(random.choice(FONTS), size = IMAGE_SIZE - 6)  # Pick a random font
    img = Image.new('L', (IMAGE_SIZE, IMAGE_SIZE), color = 255)   # 'L' means grayscale
    draw = ImageDraw.Draw(img)
    (text_width, text_height) = draw.textsize(rank, font = font)  # Extract text size
    draw.text(((IMAGE_SIZE - text_width) / 2, (IMAGE_SIZE - text_height) / 2 - 4), rank, fill = 0, font = font)

    # Random rotate transformation
    img = img.rotate(random.uniform(-ROTATE_MAX_ANGLE, ROTATE_MAX_ANGLE), expand = False, fillcolor = '#FFFFFF')
    pixels = list(img.getdata())  # Extract image pixels

    # Introduce random noise
    for (i, _) in enumerate(pixels):
        if random.random() <= noise_level:
            pixels[i] = random.randint(0, 255)  # Replace a chosen pixel with a random intensity

    # Save noisy image
    noisy_img = Image.new('L', img.size)
    noisy_img.putdata(pixels)

    return noisy_img

def save_without_generate(img :Image, file_name, data_dir_feature):
    """
    Save image sperately with corresponding name.

    Arguments
    ---------
    img : Image
        Specific feature image for storing.
    file_name : string
        Specific name correspond to the feature image.
    data_dir_feature: string
        Target directory
    """

    # use to save feature image, easy to observe the result
    if not os.path.exists(data_dir_feature):
        os.makedirs(data_dir_feature)  # Generate a directory for data set storage, if not already present
    img.save(f"{data_dir_feature}\\{file_name}")  # The filename encodes the original label from training/testing