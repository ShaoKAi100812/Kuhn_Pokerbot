# <ASSIGNMENT: Define and interact with your model. Motivate your choices in the docstrings and comments. This file
# contains a suggested structure; you are free to define your own structure, adjust function arguments etc. Don't forget
# to write appropriate tests for your functionality.>
import tensorflow as tf
from tensorflow.keras import layers, models

from data_sets import *

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'   # turn off GPU

def build_model():
    """
    Prepare the model.

    Returns
    -------
    model : model class from any toolbox you choose to use.
        Model definition (untrained).
    """
    # conv layers
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    # fully connected layers
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(4, activation='softmax'))

    return model

def train_model(model, n_validation, write_to_file=False):
    """
    Fit the model on the training data set.

    Arguments
    ---------
    model : model class
        Model structure to fit, as defined by build_model().
    n_validation : int
        Number of training examples used for cross-validation.
    write_to_file : bool
        Write model to file; can later be loaded through load_model().

    Returns
    -------
    model : model class
        The trained model.
    """
    model.compile(optimizer='adam',  # Optimizer
              # CategoricalCrossentropy for one-hot coding
              loss=tf.keras.losses.CategoricalCrossentropy(),       
              # List of metrics to monitor
              metrics=['accuracy'])
    training_features, training_labels, validation_features, validation_labels = load_data_set(TRAINING_IMAGE_DIR, n_validation)
    model.fit(training_features.astype('float32'), training_labels, batch_size=64, epochs=10, 
                validation_data=(validation_features.astype('float32'), validation_labels)) 
    # Store MyModel in the target directory
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if write_to_file == True:
        model.save(f"{MODEL_DIR}\\MyModel")
        print("Model Saved!")

    return model


def load_model():   
    """
    Load a model from file.

    Returns
    -------
    model : model class
        Previously trained model.
    """
    model = tf.keras.models.load_model(f"{MODEL_DIR}\\MyModel")

    return model

def evaluate_model(model, data_dir):
    """
    Evaluate model on the test set.

    Arguments
    ---------
    model : model class
        Trained model.
    data_dir : str
        Directory for using specific dataset to evaluate model.

    Returns
    -------
    score : float
        A measure of model performance.
    """
    test_features, test_labels, _, _ = load_data_set(data_dir)
    scores = model.evaluate(test_features, test_labels)[1]

    return scores


def identify(image, model):
    """
    Use model to classify a single card image.

    Arguments
    ---------
    image : Image
        Image to classify.
    model : model class
        Trained model.

    Returns
    -------
    rank : str in ['J', 'Q', 'K', 'A']
        Estimated card rank.
    """
    # identify one image each time
    features = extract_features(image).reshape(1, 32, 32, 1)    # reshape the feature into four dimensions for model input
    prediction = model.predict(features)
    rank = LABELS[np.argmax(prediction[0])]     # Extract the highest expectation within JQKA by max argument
    
    return rank
