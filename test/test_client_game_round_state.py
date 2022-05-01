import conftest
from client.state import ClientGameRoundState

# create an instance for validation
client_test = ClientGameRoundState(1,1)

# <ASSIGNMENT: Test the creation, reading and updating of ClientGameRoundState>
class TestClientGameRoundState:
    
    # validate creation of ClientGameRoundState
    def test_creation(self):
        # validate creation of set_card() 
        client_test.set_card('J')
        assert client_test._card == 'J'
        # validate creation of set_card_image()
        client_test.set_card_image(conftest.image)
        assert client_test._card_image == conftest.image
        # validate creation of set_turn_order()
        client_test.set_turn_order(1)
        assert client_test._turn_order == 1
        # validate creation of set_moves_history()
        client_test.set_moves_history(['CHECK', 'BET'])
        assert client_test._moves_history == ['CHECK', 'BET']
        # validate creation of set_available_actions()
        client_test.set_available_actions(['BET', 'CHECK'])
        assert client_test._available_actions == ['BET', 'CHECK']
        # validate creation of set_outcome()
        client_test.set_outcome('DEFEAT')
        assert client_test._outcome == 'DEFEAT'
        # validate creation of set_cards()
        client_test.set_cards('JK')
        assert client_test._cards == 'JK' 
    
    # validate reading of ClientGameRoundState
    def test_reading(self):
        # validate creation of get_coordinator_id() 
        assert client_test.get_coordinator_id
        # validate creation of get_round_id() 
        assert client_test.get_round_id() == 1
        # validate creation of get_card() 
        client_test.set_card('Q')
        assert client_test.get_card() == 'Q'
        # validate creation of get_card_image()
        client_test.set_card_image(conftest.image)
        assert client_test.get_card_image() == conftest.image
        # validate creation of get_turn_order()
        client_test.set_turn_order(2)
        assert client_test.get_turn_order() == 2
        # validate creation of get_move_history()
        client_test.set_moves_history(['CHECK', 'CHECK'])
        assert client_test.get_moves_history() == ['CHECK', 'CHECK']
        # validate creation of get_available_actions()
        client_test.set_available_actions(['CALL', 'FOLD'])
        assert client_test.get_available_actions() == ['CALL', 'FOLD']
        # validate creation of get_outcome()
        client_test.set_outcome('DEFEAT')
        assert client_test.get_outcome() == 'DEFEAT'
        # validate creation of get_cards()
        client_test.set_cards('QA')
        assert client_test.get_cards() == 'QA'

    # validate updating of ClientGameRoundState
    def test_updating(self):
        # validate update of add_move_history()
        client_test.set_moves_history(['CHECK', 'BET'])
        client_test.add_move_history('BET')
        assert client_test._moves_history[len(client_test._moves_history) - 1] == 'BET'