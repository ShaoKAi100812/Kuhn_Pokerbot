import os
import pytest
from PIL import Image


TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TRAINING_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "training_images")
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")

# Pseudo string for server simulation
TEST_PLAYER_TOKEN = 'KobeBryant'
TEST_COORDINATOR_ID = 'SteveJobs'
TEST_PLAYER_BANK = 5
TEST_TURN_ORDER_1 = 1
TEST_TURN_ORDER_2 = 2
TEST_MOVES_HISTORY = [[],'BET','Michael']#[] for player1,others for player2

# Context to retain objects passed between steps
class Context:
    pass

@pytest.fixture(scope='session')
def context():
    return Context()

@pytest.fixture()
def image(request):
    return Image.open(os.path.join(TEST_IMAGE_TEST_DIR, "J.jpg"))

# <ASSIGNMENT: Define your own fixtures for testing here>
