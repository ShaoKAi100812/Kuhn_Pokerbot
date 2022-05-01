from calendar import c
import random
from tracemalloc import start

from matplotlib.pyplot import get
from model import load_model, identify
from client.state import ClientGameRoundState, ClientGameState
import numpy as np
import time
import os

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# using state to get card: True. Set to False when identify() is finished.
# COORDINATOR_REVEAL_CARDS in ./server/dev/setting.py also need to be set False.
GET_CARD = False

class PokerAgent(object):

    def __init__(self,game_type):
        self._model = load_model()
        self._estimated_card = None
        self._game_type = game_type # Game type: str in ['3','4']
        self._conf = [[],[]] # self.conf[0] for player1, self.conf[1] for player 2
        self._decay = []
        self._logFilePath = os.path.dirname(os.path.abspath(__file__))+'\\log\\'+time.strftime('%d-%m-%Y-%H-%M-%S.txt',time.localtime())

    def make_action(self, state: ClientGameState, round: ClientGameRoundState) -> str:
        """
        Next action, used to choose a new action depending on the current state of the game. This method implements your
        unique PokerBot strategy. Use the state and round arguments to decide your next best move.
        Parameters
        ----------
        state : ClientGameState
            State object of the current game (a game has multiple rounds)
        round : ClientGameRoundState
            State object of the current round (from deal to showdown)
        Returns
        -------
        str in ['BET', 'CALL', 'CHECK', 'FOLD'] (and in round.get_available_actions())
            A string representation of the next action an agent wants to do next, should be from a list of available actions
        """
        # <ASSIGNMENT: Replace this random strategy with your own implementation and update file(s) accordingly. Make
        # your implementation robust against the introduction of additional players and/or cards.>

        #wait for response
        time.sleep(0.1)

        current_bank = state.get_player_bank()
        # When current bank<2, confidence to bet is 1.
        if int(current_bank) < 2:
            self.get_conf()[0][0],self.get_conf()[1][0] = 0,0
        # Set back conf for J to 1 when current bank >= 2.
        else:
            self.get_conf()[0][0],self.get_conf()[1][0] = 1,1

        # Get availabel actions
        available_actions = round.get_available_actions()
        print(available_actions)

        #use current system time as seed for random
        random.seed()
        flag = random.random()

        # Get turn 
        turn_order =  round.get_turn_order() # int
        if turn_order == None:
            turn_order = 1
        print(f'Turn Order:{turn_order}')

        # Switching between round.get_card() and identify() in model
        # TODO:Only leave in branch dev. Should be pruned in release version.
        if GET_CARD:
            if round.get_card() == 'J':
                    conf = self.get_conf()[turn_order-1][0]
                    decay = self._decay()[0]
            if round.get_card() == 'Q':
                    conf = self.get_conf()[turn_order-1][1]
                    decay = self.get_decay()[1]
            if round.get_card() == 'K':
                    conf = self.get_conf()[turn_order-1][2]
                    decay = self.get_decay()[2]
            if (self.get_game_type() == '4') and (round.get_card() == 'A'):
                decay =self.get_decay()[3]
                conf = self.get_conf()[turn_order-1][3]
            current_card = round.get_card()
            try:
                current_card in ['J', 'Q', 'K', 'A']
            except Exception:
                print("Inavailable Input!")
                self.on_error("Inavailable Input!")
            print(current_card)   
        else:
            current_card = self.get_estimated_card()
            
            # In case of make action is called before on image, set current card to 'J' to be more cautions.
            if current_card == None:
                current_card = 'Q'
            print(f'Current card:{current_card}')
            if not current_card in ['J', 'Q', 'K', 'A']:
                self.on_error("Inavailable Input!")            
            if current_card == 'J':
                conf = self.get_conf()[turn_order-1][0]
                decay = self.get_decay()[0]
            if current_card == 'Q':
                conf = self.get_conf()[turn_order-1][1]
                decay = self.get_decay()[1]
            if current_card == 'K':
                conf = self.get_conf()[turn_order-1][2]
                decay = self.get_decay()[2]
            if (self.get_game_type() == '4') and (current_card == 'A'):
                decay =self.get_decay()[3]
                conf = self.get_conf()[turn_order-1][3]
        
        if len(round.get_moves_history()) == 0 or round.get_moves_history()[len(round.get_moves_history()) - 1] == 'CHECK':
            # available = ['BET', 'CHECK']
            #update conf with decay. Opponent CHECK, then the possibility to BET is bigger.
            conf = conf/decay
            if flag > conf and 'BET' in available_actions:
                return 'BET' # 'BET'
            if flag <= conf and 'CHECK' in available_actions: 
                return 'CHECK'
        else:
            # update conf with decay, if opponent bet then conf is larger, the possibility to bet or call will be smaller 
            if round.get_moves_history()[len(round.get_moves_history()) - 1] == 'BET':
                conf = conf*decay
            else:
                conf = conf/decay
            # available = ['FOLD', 'CALL','BET]
            if flag > conf and 'CALL' in available_actions:
                return 'CALL'
            if flag > conf and 'BET' in available_actions:
                return 'BET'
            if flag <= conf and 'FOLD' in available_actions:
                return 'FOLD'
        # In case anything wrong happened
        return random.choice(available_actions)

    def get_game_type(self):
        return self._game_type

    def set_game_type(self,game_type:str):
        self._game_type = game_type

    def on_image(self, image):
        """
        This method is called every time when card image changes. Use this method for image recongition procedure.
        Parameters
        ----------
        image : Image
            Image object
               
        """
        try:
            # Switching between round.get_card() and identify() in model
            # TODO:Only leave in branch dev. Should be pruned in release version.
            if GET_CARD:
                print("Before finishing the identify(), we use get_card().")
            else:
                self.set_estimated_card(identify(image,self._model))

            # if identify failed, set card to J to be more cautious.
            if self.get_estimated_card == None:
                print("Identify failed. Set card as J.")
                self.set_estimated_card('J')
        except Exception:
            self.on_error("on image error")

    def set_estimated_card(self, card:str):
        """
        Setter for attribute estimated_card.
        Only used for complimentation.
        """
        self._estimated_card = card

    def get_estimated_card(self):
        """
        Getter for attribute estimated_card
        """
        return self._estimated_card
        
    def get_conf(self):
        """
        Getter for attribute conf
        """
        return self._conf
    def get_decay(self):
        """
        getter for attribute decay
        """
        return self._decay
    def get_logFilePath(self):
        return self._logFilePath


    def on_error(self, error):
        """
        This methods will be called in case of error either from server backend or from client itself. You can
        optionally use this function for error handling.
        Log errors and raise error.
        Parameters
        ----------
        error : str
            string representation of the error
        """
        logFile = open(self._logFilePath,'a')
        logFile.write('\nLogging error ...\n')
        logFile.write('Error: '+error+'\n')
        logFile.close()
        raise Exception(error)

    def on_game_start(self):
        """
        This method will be called once at the beginning of the game when server confirms both players have connected.
        Check whether .\log folder exists or not. If not then make one.
        Initialize the conf and decay array.
        Parameters
        ----------
        NULL
        
        Returns
        -------
        NULL
        """
        if not os.path.exists(f'{AGENT_DIR}\\log'):
            os.mkdir(f'{AGENT_DIR}\\log')
        try:
            self.__init_conf_decay()
        except Exception:
            self.on_error("On_game_start() error.")

    def on_new_round_request(self, state: ClientGameState):
        """
        This method is called every time before a new round is started. A new round is started automatically.
        You can optionally use this method for logging purposes.
        ---------
        Parameters
        ----------
        state : ClientGameState
            State object of the current game
        """
        try:
            logFile = open(self._logFilePath,'a')
            logFile.write('\nLogging at new round ...\n')
            logFile.write('Coordinator ID: '+ state.get_coordinator_id()+'.\n')
            logFile.write('Player token: '+state.get_player_token()+'.\n')
            logFile.close()
        except Exception:
            self.on_error("On_new_round_request() error.")

    def on_round_end(self, state: ClientGameState, round: ClientGameRoundState):
        """
        This method is called every time a round has ended. A round ends automatically. You can optionally use this
        method for logging purposes.
        Log last round win or lose, if any.
        Update current decay.
        Log current decay.
        Parameters
        ----------
        state : ClientGameState
            State object of the current game
        round : ClientGameRoundState
            State object of the current round
        """
        try:
            round = state.get_last_round_state()
            logFile = open(self._logFilePath,'a')
            logFile.write('\nLogging at round end...\n')
            logFile.write('Round: '+str(round.get_round_id())+'\n')
            # logFile.write('Coordinator ID: '+ round.get_coordinator_id()+'.\n')
            # logFile.write('Player token: '+state.get_player_token()+'.\n')
            logFile.write('Turn order:'+str(round.get_turn_order())+'. Card in hand: '+self.get_estimated_card()+'.\n')
            #ask model team how do they deal with the binary image
            if round.is_ended():
                logFile.write('Move history: '+','.join(round.get_moves_history())+'\n')
                logFile.write('Outcome: '+ str(round.get_outcome())+'. Cards for both players:'+str(round.get_cards())+'.\n')
                # Update decay at round end
                self.__update_decay(str(round.get_outcome()),round.get_moves_history()[-1])
                # Log decay
                logFile.write('Decay: '+','.join(str(i) for i in self.get_decay()))
                logFile.write(f'\nCurrent Bank:{state.get_player_bank()}.\n')
                print(f'Current Bank:{state.get_player_bank()}.\n')
            # Save logFile
            logFile.close()
        except Exception:
            self.on_error('On_round_end() error.')

        # print(round.get_round_id(), f'[{round.get_card()}|{round.get_turn_order()}]', ':', round.get_moves_history(), '->',
        #       f'{round.get_outcome()}|{round.get_cards()}')

    def on_game_end(self, state: ClientGameState, result: str):
        """
        This method is called once after the game has ended. A game ends automatically. You can optionally use this
        method for logging purposes.
        Format:Filename: Game start time
        Result:str,Bank:str
        Parameters
        ----------
        state : ClientGameState
            State object of the current game
        result : str in ['WIN', 'DEFEAT']
            End result of the game
        """
        try:
            logFile = open(self._logFilePath,'a')
            current_bank = state.get_player_bank()
            logFile.write(f'\nLogging at game end...\nResult: {result}.\nCurrent bank:{current_bank}.\n')
            print(f'Result:{result}')
            # Save logFile
            logFile.close()

        except Exception:
            self.on_error('On_game_end() error.')
    
    def __init_conf_decay(self):
        """
        This method is called at game start to initialize conf and decay
        array according to the game type ['3','4'].
        The array is in the order of ['J','Q','K','A'(if game type='4')]
        Tune the numbers for Q and K to raise possibility to win.
        """
        if self.get_game_type() == '3':
            self._conf[0] = np.array([0.95,0.55,0.1])
            self._conf[1] = np.array([0.95,0.55,0.1])
            self._decay = np.array([1,1.2,1])           
        else:
            self._conf[0] = np.array([0.95,0.7,0.25,0.1])
            self._conf[1] = np.array([0.95,0.7,0.25,0.1])
            self._decay = np.array([1,1.15,1.2,1])

    def __update_decay(self,outcome:str,last_move:str):
        # Player lose with last move "BET" or "CALL", increase decay for Q or QK to be more cautions.
        # upper bound is 1.5
        if int(outcome) < 0 and last_move in ['BET','CALL']:
            if self.get_game_type() == '3':
                self._decay[1] = self._decay[1]*1.05 if self._decay[1]*1.05<=1.5 else self._decay[1]
            elif self.get_game_type() == '4':
                self._decay[1] = self._decay[1]*1.05 if self._decay[1]*1.05<=1.5 else self._decay[1]                   
                self._decay[2] = self._decay[2]*1.05 if self._decay[2]*1.05<=1.5 else self._decay[2]
        # Player lose with last move "FOLD", reduce decay for Q or QK to be more bold.
        # lower bound is 1.05
        if int(outcome) < 0 and last_move == 'FOLD':
            if self.get_game_type() == '3':
                self._decay[1] = self._decay[1]*0.95 if self._decay[1]*0.95>=1.05 else self._decay[1]
            elif self.get_game_type() == '4':
                self._decay[1] = self._decay[1]*0.95 if self._decay[1]*0.95>=1.05 else self._decay[1]                   
                self._decay[2] = self._decay[2]*0.95 if self._decay[2]*0.95>=1.05 else self._decay[2]

        # Player win with last move "BET" or "CALL", decrease decay for Q or QK to be more brave.
        # lower bound is 1.05
        if int(outcome) > 0 and last_move in ['BET','CALL']:
            if self.get_game_type() == '3':
                self._decay[1] = self._decay[1]*0.95 if self._decay[1]*0.95>=1.05 else self._decay[1]
            elif self.get_game_type() == '4':
                self._decay[1] = self._decay[1]*0.95 if self._decay[1]*0.95>=1.05 else self._decay[1]                   
                self._decay[2] = self._decay[2]*0.95 if self._decay[2]*0.95>=1.05 else self._decay[2]
        # Player lose with last move "FOLD", increase decay for Q or QK to be more cautious.
        # upper bound is 1.5
        if int(outcome) > 0 and last_move == 'FOLD':
            if self.get_game_type() == '3':
                self._decay[1] = self._decay[1]*1.05 if self._decay[1]*1.05<=1.5 else self._decay[1]
            elif self.get_game_type() == '4':
                self._decay[1] = self._decay[1]*1.05 if self._decay[1]*1.05<=1.5 else self._decay[1]                   
                self._decay[2] = self._decay[2]*1.05 if self._decay[2]*1.05<=1.5 else self._decay[2]
