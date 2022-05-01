from data_sets import *
import shutil

TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")
TEST_IMAGE_GEN_DIR = os.path.join(TEST_DIR, "data_sets", "generate_images")

FILE_NAME = "A_1.png"
TEST_IMAGE = Image.open(f"{TEST_IMAGE_TEST_DIR}\\{FILE_NAME}")
N_SAMPLE = random.randint(1, 10)
RANK = random.choice(LABELS)

class TestDataSets:
    # <ASSIGNMENT: Test the extract_features(), load_data_set() and generate_noisy_image() functions in
    # data_sets.py. You can use the images under the test\data_sets\ directories for unit testing.
    # You don't need to test generate_data_set().>

    def test_extract_features(self):    
        feature = extract_features(TEST_IMAGE)
        # Test size
        assert len(np.shape(feature)) == 3      # Dimension test
        assert np.shape(feature)[0] == IMAGE_SIZE
        assert np.shape(feature)[1] == IMAGE_SIZE
        # Test value
        for i in range(IMAGE_SIZE):
            for j in range(IMAGE_SIZE):
                assert feature[i][j] in [0, 1]

    def test_load_data_set(self):
        features, labels, _, _= load_data_set(TEST_IMAGE_TEST_DIR)
        # Test size
        assert len(np.shape(features)) == 4     # Dimension test
        assert len(np.shape(labels)) == 2       # Dimension test
        assert np.shape(features)[1] == IMAGE_SIZE
        assert np.shape(features)[2] == IMAGE_SIZE
        assert np.shape(labels)[1] == len(LABELS)
        # Test feature value
        features = np.reshape(features, -1)
        for i in range(len(features)):
            assert features[i] in [0, 1]
        # Test one-hot coding
        for i in range(np.shape(labels)[0]):
            counter = 0
            for j in range(np.shape(labels)[1]):
                if labels[i][j] == 1:
                    counter += 1
            assert counter == 1

    def test_generate_data_set(self):
        generate_data_set(N_SAMPLE, TEST_IMAGE_GEN_DIR)
        # Test sample generation
        assert len(os.listdir(TEST_IMAGE_GEN_DIR)) == N_SAMPLE
        # Delete the testing file
        if os.path.exists(TEST_IMAGE_GEN_DIR):  # Sanity check
            shutil.rmtree(TEST_IMAGE_GEN_DIR)

    def test_generate_noisy_image(self):
        noise_img = generate_noisy_image(RANK, random.random())
        # Test data type
        assert isinstance(noise_img, Image.Image)
        # Test data size
        assert noise_img.size == (IMAGE_SIZE, IMAGE_SIZE)
    
    def test_save_without_generate(self):
        save_without_generate(TEST_IMAGE, FILE_NAME, TEST_IMAGE_GEN_DIR)
        # Test sample storage
        assert os.listdir(TEST_IMAGE_GEN_DIR)[0] == FILE_NAME
        # Delete the testing file
        if os.path.exists(TEST_IMAGE_GEN_DIR):  # Sanity check
            shutil.rmtree(TEST_IMAGE_GEN_DIR)
