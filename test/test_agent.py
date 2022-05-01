from agent import PokerAgent
import pytest
import os
from client.state import ClientGameRoundState, ClientGameState

# Pseudo value for server response
TEST_PLAYER_TOKEN = 'KobeBryant'
TEST_COORDINATOR_ID = 'SteveJobs'
TEST_PLAYER_BANK = 5
TEST_GAMETYPE = '3'

#initialize with 3 cards game
TEST_AGENT = PokerAgent(TEST_GAMETYPE)
TEST_STATE = ClientGameState(TEST_COORDINATOR_ID,TEST_PLAYER_TOKEN,TEST_PLAYER_BANK)
TEST_ROUND_1 = ClientGameRoundState(TEST_COORDINATOR_ID,'1')
TEST_ROUND_2 = ClientGameRoundState(TEST_COORDINATOR_ID,'2')

# TEST_IMAGE feed in
TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")
ROOT_DIR = os.path.abspath(os.path.join(TEST_DIR,"../.."))

class TestPokerAgent:
    # <ASSIGNMENT: Test agent initialization and the make_action() function. Also test logging and error handling if you
    # chose to use them.>

    def test_init(self):
        """
        Test agent initialization
        """
        assert TEST_AGENT.get_estimated_card() == None
        assert len(TEST_AGENT.get_conf()) == 2
        assert len(TEST_AGENT.get_decay()) == 0
        assert type(TEST_AGENT.get_logFilePath()).__name__ == 'str'
        assert TEST_AGENT.get_game_type() == TEST_GAMETYPE

    def test_on_game_start(self):
        """
        Test conf and decay array initialization.
        Test make_action().
        """
        TEST_AGENT.on_game_start()
        assert os.path.exists('log') == True
        #Test len(conf) and len(decay) intialized accoridng to GAMETYPE in ["3","4"]
        assert len(TEST_AGENT.get_conf()[0]) == int(TEST_GAMETYPE)
        assert len(TEST_AGENT.get_conf()[1]) == int(TEST_GAMETYPE)
        assert len(TEST_AGENT.get_decay()) == int(TEST_GAMETYPE)

        # set round attribute to test player 1 making action 
        TEST_AGENT.on_game_start()
        TEST_AGENT.set_estimated_card('J')
        TEST_ROUND_1.set_available_actions(['CHECK','BET'])
        TEST_ROUND_1.set_turn_order(1)
        assert TEST_AGENT.make_action(TEST_STATE,TEST_ROUND_1) in ['CHECK','BET']
        
        # test invalid card identify result
        TEST_AGENT.set_estimated_card('?')
        assert pytest.raises(Exception,TEST_AGENT.make_action,TEST_STATE,TEST_ROUND_1)
        
        #set round attribute to test player 2 making action
        #first move was 'BET'
        TEST_AGENT.set_game_type('4')
        TEST_AGENT.on_game_start()
        TEST_AGENT.set_estimated_card('A')
        TEST_ROUND_2.set_available_actions(['BET','FOLD'])
        TEST_ROUND_2.add_move_history('BET')
        TEST_ROUND_2.set_turn_order(2)
        assert TEST_AGENT.make_action(TEST_STATE,TEST_ROUND_2) in ['BET','FOLD']

        #test if bank<2 & card='J', action='BET'
        TEST_AGENT.set_estimated_card('J')
        TEST_STATE.update_bank('-4')
        assert TEST_AGENT.make_action(TEST_STATE,TEST_ROUND_1) == 'BET'

    def test_error_handeling(self):
        """
        Test on_error()
        """
        assert pytest.raises(Exception, TEST_AGENT.on_error,'TestError')
    
    def test_logging(self):
        """"
        Test logging at game end.
        """
        TEST_AGENT.on_game_start()
        TEST_STATE.update_bank('2')
        TEST_AGENT.on_game_end(TEST_STATE,'WIN')
        assert os.path.exists(TEST_AGENT.get_logFilePath())