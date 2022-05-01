import client.state

# Pseudo value for server response
TEST_PLAYER_TOKEN = 'KobeBryant'
TEST_COORDINATOR_ID = 'SteveJobs'
TEST_PLAYER_BANK = 5

# create an instance for validation
test_client = client.state.ClientGameState(TEST_COORDINATOR_ID,TEST_PLAYER_TOKEN,TEST_PLAYER_BANK)

# <ASSIGNMENT: Test the creation, reading and updating of ClientGameState>
class TestClientGameState:
    def test_client_game_state_init(self):
        # validate creation of ClientGameState
        assert test_client.get_coordinator_id() == TEST_COORDINATOR_ID
        assert test_client.get_player_token() == TEST_PLAYER_TOKEN
        assert test_client.get_player_bank() == TEST_PLAYER_BANK
    
    def test_client_game_state_start_new_round(self):
        #validate start_on_new_round() and get_rounds() of ClientGameState
        test_client.start_new_round()
       #validate get_last_round_state()
        assert test_client.get_last_round_state().__class__.__name__ == 'ClientGameRoundState'
        assert type(test_client.get_rounds()).__name__ == 'list'

    def test_client_game_state_update_bank(self):
        #validate updating
        test_client.update_bank('-1')
        assert test_client.get_player_bank() == TEST_PLAYER_BANK-1