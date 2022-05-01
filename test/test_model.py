import os
from model import *
from PIL import Image

TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")

TEST_MODEL = load_model()
TEST_IMAGE = Image.open(f"{TEST_IMAGE_TEST_DIR}\\A_1.png")

class TestModel:
    # <ASSIGNMENT: Test the build_model(), load_model() and evaluate_model() functions in model.py. You can use the
    # images under the test\data_sets\ directories for unit testing. You don't need to test train_model().>
    
    def test_build_model(self):
        # Test model building successfully
        assert build_model().__class__.__name__ == 'Sequential'
    
    def test_load_model(self):
        # Test model loading successfully
        assert load_model().__class__.__name__ == 'Sequential'

    def test_evaluate_model(self):
        # Test return between 0 to 1
        assert evaluate_model(TEST_MODEL,TEST_IMAGE_TEST_DIR) >= 0
        assert evaluate_model(TEST_MODEL,TEST_IMAGE_TEST_DIR) <= 1

    def test_identify(self):
        # Test return str belongs to JQKA
        assert identify(TEST_IMAGE, TEST_MODEL) in LABELS
