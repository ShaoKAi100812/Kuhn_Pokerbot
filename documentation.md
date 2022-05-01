# Documentation for the PokerBot of Group 15

---
  - [Project Introduction](#project-introduction)
    - [Game Introduction](#game-introduction)
    - [Implementation Approach](#implementation-approach)
      - [Data Sets and Model](#data-sets-and-model)

      - [Agent and Strategy](#agent-and-strategy)

    - [Preparation](#preparation)
    - [Tutorial](#tutorial)
  - [Software implementation](#software-implementation)
    - [data_sets](#data_sets)
    - [model](#model)
    - [agent](#agent)
  - [Project management](#project-management)
    - [Project Planning](#project-planning)
    - [Project Execution](#project-execution)
    - [Project Monitoring](#project-monitoring)
    - [Project Control](#project-control)
  - [Reference](#reference)
---

## Project Introduction
In this project, our aim is to design and program a pokerbot which is able to participate in a Kuhn Poker game with others. By classifying the received cards, it is supposed to make suitable actions based on our own designed strategy.

### Game Introduction
Kuhn Poker is an extremely simplified poker game. As a simple model zero-sum two-player imperfect-information game, it is amenable to a complete game-theoretic analysis. More details of its rules will be introduced in our agent and strategy part.

### Implementation Approach
To achieve the goal, our task is divided into two main parts. One part is to build and train a model to classify the cards given by the server. The other is to develop an agent with a suitable strategy to make actions after receiving these cards. Details are introduced as follow.

#### Data Sets and Model
##### 1. Dataset
- __Initial Condition Setup__
Set the parameters noise level = 0.7 and rotation = 180.  
Generate 5000 training data and 1000 testing data with noise level randomly between 0 to 0.7 and rotation degree randomly between 0 to 180.  

&emsp;&emsp;For examples:  

&emsp;&emsp;![A_9](https://user-images.githubusercontent.com/62060031/162200550-9c0c6755-6780-4b3e-abeb-f05a2808d0ba.png) ![A_12](https://user-images.githubusercontent.com/62060031/162200570-fc444633-a71b-4703-a40a-10cfe5afbb5e.png) ![A_33](https://user-images.githubusercontent.com/62060031/162203083-939971f1-7312-4e8f-b122-9993e7e3ae8e.png) ![A_36](https://user-images.githubusercontent.com/62060031/162200593-4b6a2d54-acc9-4636-8328-21f217caf494.png)  
&emsp;&emsp;![J_2](https://user-images.githubusercontent.com/62060031/162200694-6900e494-9fb3-49a3-ba10-a7664312ab5b.png) ![J_7](https://user-images.githubusercontent.com/62060031/162200704-3a7c678c-883a-45df-b2d3-9d18a1da0607.png) ![J_14](https://user-images.githubusercontent.com/62060031/162200723-e5a2aaf3-a62c-41ae-8fdb-52725045a23a.png) ![J_42](https://user-images.githubusercontent.com/62060031/162204930-03b20e27-da5f-4b5d-a548-0030afc40f41.png)  
&emsp;&emsp;![K_21](https://user-images.githubusercontent.com/62060031/162200843-55811459-95b1-4d88-8d7e-dc99b49496a4.png) ![K_39](https://user-images.githubusercontent.com/62060031/162200864-c98d046f-d1aa-4710-8e77-ea5bcb88ff55.png) ![K_75](https://user-images.githubusercontent.com/62060031/162200873-655c15bf-c370-4dd5-ae3e-5df8d532e02b.png) ![K_119](https://user-images.githubusercontent.com/62060031/162200886-470f3f40-256b-44ba-bb78-a58047fdb15b.png)  
&emsp;&emsp;![Q_0](https://user-images.githubusercontent.com/62060031/162200956-586cfa5b-2100-482c-9621-6239b6021bd7.png) ![Q_19](https://user-images.githubusercontent.com/62060031/162200972-3a39da06-be3e-4f89-b647-f8c3c8b7464d.png) ![Q_49](https://user-images.githubusercontent.com/62060031/162201022-3a69889f-8f67-4fea-b540-fa52e1fb5d3f.png) ![Q_56](https://user-images.githubusercontent.com/62060031/162201033-15c054ba-5111-4875-bc84-f52f83c95ca0.png)

- __Feature Extraction Process__
Except change the value from analog (0 to 255) to digital (0 and 1), also apply noise cancellation in the extraction process.  
Step 1: Apply a light Gaussian Blur  
Step 2: Apply a loose single-value threshold to filter some light noise out  
Step 3: Apply a 3x3 averaging kernel to get a stronger blur effect  
Step 4: Apply a hysteresis threshold to nicely keep the shape of words

- __Result Comparison__  
&ensp;&ensp;&ensp;&ensp;**Before / After**  
**A_9**: &ensp;![A_9](https://user-images.githubusercontent.com/62060031/162200550-9c0c6755-6780-4b3e-abeb-f05a2808d0ba.png)&ensp;&ensp;![A_9](https://user-images.githubusercontent.com/62060031/162201328-a4d4a87e-abd3-465e-88d9-fb7b1e40b8ab.png)  
**A_12**: ![A_12](https://user-images.githubusercontent.com/62060031/162200570-fc444633-a71b-4703-a40a-10cfe5afbb5e.png)&ensp;&ensp;![A_12](https://user-images.githubusercontent.com/62060031/162202585-90611985-89ae-4d62-a81a-cf3736415ae8.png)  
**J_14**: ![J_14](https://user-images.githubusercontent.com/62060031/162200723-e5a2aaf3-a62c-41ae-8fdb-52725045a23a.png)&ensp;&ensp;![J_14](https://user-images.githubusercontent.com/62060031/162204108-77ff88d6-1122-4e3f-8b75-a6f04adaa9b2.png)  
**J_42**: ![J_42](https://user-images.githubusercontent.com/62060031/162204930-03b20e27-da5f-4b5d-a548-0030afc40f41.png)&ensp;&ensp;![J_42](https://user-images.githubusercontent.com/62060031/162205032-289eb9d7-9f00-4642-9476-274ec81b9e2a.png)  
**K_39**: ![K_39](https://user-images.githubusercontent.com/62060031/162200864-c98d046f-d1aa-4710-8e77-ea5bcb88ff55.png)&ensp;&ensp;![K_39](https://user-images.githubusercontent.com/62060031/162205764-2e7e1810-b62b-4250-a442-97f5eb198591.png)  
**K_75**: ![K_75](https://user-images.githubusercontent.com/62060031/162200873-655c15bf-c370-4dd5-ae3e-5df8d532e02b.png)&ensp;&ensp;![K_75](https://user-images.githubusercontent.com/62060031/162205957-92087a4b-f7fa-471e-8b0e-b70ea6ba75ed.png)  
**Q_49**: ![Q_49](https://user-images.githubusercontent.com/62060031/162201022-3a69889f-8f67-4fea-b540-fa52e1fb5d3f.png)&ensp;&ensp;![Q_49](https://user-images.githubusercontent.com/62060031/162206204-28c42e96-6608-40cb-a73e-0ee8a98a342d.png)  
**Q_56**: ![Q_56](https://user-images.githubusercontent.com/62060031/162201033-15c054ba-5111-4875-bc84-f52f83c95ca0.png)&ensp;&ensp;![Q_56](https://user-images.githubusercontent.com/62060031/162206275-9f821f3c-15bb-436a-9ffc-ff7c1ec0f4e8.png)  

##### 2. Model
- __Destination__
Classify four different cards `J Q K A` by using 32x32 pixel images.
- __Model Architecture__ 
Based on the concept of VGG structure, use TensorFlow package to create a small five-layer CNN model.  
Due to the easy classification task, only use three convolution layers to extract the feature and two fully connected layers to fulfill the goal.  
Take ReLU as the activation layer after each convolution layer and fully connected layer, except the last layer.  
Also, apply 2x2 max pooling layer after each convolution layer.
At the end, apply Softmax as the activation function at the last layer to cooperate with cross-entropy loss function due to the one-hot coding labels.  
![image](https://user-images.githubusercontent.com/62060031/162096321-e20e0d71-54fe-4319-bf90-f1a207fdb602.png)

- __Traning Result__
With 5000 training data and 1000 testing generated by 0-180 degree rotation and 0-0.7 noise level, our testing accurcy is 0.973.  
It is robust enough to deal with high noisy inputs and still perform very well.


#### Agent and Strategy
##### 1. Game Rules
* Check <https://en.wikipedia.org/wiki/Kuhn_poker>.
* Note that there is a difference between our project and the game introduced in Wikipedia. In this project, the cards can be 3 or 4, which is set by the backend.

##### 2. Strategy Idea
* The confidence of BET or CALL is different for different card in hand, last move and outcome from last round.
* For example, the confidence of BET while having "J" in hand is small. And the confidence of BET is large for "A" or "K" in hand.
* When last move is BET, the confidence of BET should be smaller than before for the purpose of being cautious. Vice versa. This is achieved by multiplying or dividing a number bigger than 1. It is called decay.
* When outcome from last round is negative and last move is BET or CALL, then the confidence of BET is smaller to be more cautious. Vice versa. This is achieved by updating the decay.
* While making actions, a random number flag in (0,1) is created. If flag > confidence, then we BET or CALL. Otherwise, we CHECK or FOLD.
* Decay will be passed to next round. Confidence remains same all the time.
* If we have J or A (or K for 3 cards game), decay will not be considered. That is, for J and A, we give a fixed confidence to bet.

##### 3. Confidence Tabel for 4 cards game
|Possibility to bet (confidence)|J|Q|K|A|
|------|------|------|------|------|
|First Action(Player1)|0.05| 0.3 |0.55|0.9|
|Second Action(Player2)|0.05|0.3*decay or 0.3/decay|0.55*decay or 0.55/decay|0.9|
|Third Action(Player1)|0.05|0.3*decay or 0.3/decay|0.55*decay or 0.55/decay|0.9|

### Preparation
Before running our codes, some pakages are needed to be installed. These pakages has been listed in requirement-linux.txt and requirement-windows.txt. More specific steps to install them have been provided in README.md.

### Tutorial
To play local game, we need to have a local `KuhnPoker` server installed and running in the background. With a token given by the local server, we can connect to it and then start our game automatically.
We can also choose to play the game with others on the public server. We have to specify a `--global` flag for the script and then wait for others to join. More details about how to realize it have also been provided in README.md.

---

## Software implementation
In this part, most of the important functions in our python files will be introduced.

### data_sets
File data_sets is used to deal with data before training, including generating training and testing data.

###### extract_features
Function extract_features converts an image to features that serve as input to the image classifier.
> __Parameters:__
> - __img:__ _Image_  
> Image to convert to features.
> - __file_name:__ _str, default = None_  
> Passing the file name to save_without_generate() to save the feature image for easy observation.

> __Returns:__
> - __featres:__ _list/matrix/structure of int, int between zero and one_  
> Extracted features in a format that can be used in the image classifier.

###### load_data_set
Function load_data_set prepares features for the images in data_dir and divide in a training and validation set.
> __Parameters:__
> - __data_dir:__ _str_  
> Directory of images to load.
> - __n_validation:__ _int, default = 0_  
> Number of images that are assigned to the validation set.

> __Returns:__
> - __featres:__ _list/matrix/structure of int, int between zero and one_  
> Extracted features in a format that can be used in the image classifier.

###### generate_data_set
Function generate_data_set generates n_samples noisy images by using generate_noisy_image(), and store them in data_dir.
> __Parameters:__
> - __n_samples:__ _int_  
> Number of train/test examples to generate.
> - __data_dir:__ _str in [TRAINING\_IMAGE\_DIR, TEST\_IMAGE\_DIR]_  
> Directory for storing images.

###### generate_noisy_image
Function generate_noisy_image generates a noisy image with a given noise corruption. This implementation mirrors how the server generates the images. However the exact server settings for noise_level and ROTATE_MAX_ANGLE are unknown.

> __Parameters:__
> - __rank:__ _str in ['J', 'Q', 'K', 'A']_  
> Original card rank.
> - __noise_level:__ _int between zero and one_  
> Probability with which a given pixel is randomized.

> __Returns:__
> - __noisy_img:__ _Image_  
> A noisy image representation of the card rank.

###### save_without_generate
Fuction save_without_generate is used to save image sperately with corresponding name.
> __Parameters:__
> - __img:__ _Image_  
> Specific feature image for storing.
> - __file_name:__ _string_  
> Specific name correspond to the feature image.
> - __data_dir_feature:__ _string_  
> Target directory.

### model
File model is used to build and train our own model for classifying card images given by the server in the games.

###### build_model
Function build_model adds convolutional layers and fully connected layers to define the model.
> __Returns:__
> - __model:__ _model class_  
> Return the untrained model.

###### train_model
Function train_model fits the model on the training data set.
> __Parameters:__
> - __model:__ _model class_  
> Model structure to fit, as defined by build_model.
> - __n_validation:__ _int_  
> Number of training examples used for cross-validation.
> - __write_to_file__ _bool_  
> Write model to file; can later be loaded through load_model.

> __Returns:__
> - __model:__ _model class_  
> Return the trained model.

###### load_model
Function load_model is used to load a model from file using load_model in keras.
> __Returns:__
> - __model:__ _model class_  
> Return the previously trained model.

###### evaluate_model
Function evaluate_model evaluates our model on the test set.
> __Parameters:__
> - __model:__ _model class_  
> Model structure to fit, as defined by build_model.
> - __data_dir:__ _int_  
> Number of training examples used for cross-validation.

> __Returns:__
> - __score:__ _float_  
> Return a measure of model performance.

###### identify
The function identify uses the trained model to classify a single card image.
> __Parameters:__
> - __image:__ _Image_  
> Image to classify.
> - __model:__ _model class_  
> Trained model.

### agent
File agent is used to make actions based on our designed strategy in the game. Some important functions used in agent are introduced in the following.

###### \_\_init__
Function \_\_init__ is use to load our trained model, determine the game type and initialize other parameters in our agent.
> __Parameters:__
> - __game_type:__ _str, {'3', '4'}_  
> The parameter _game_type_ determines how many cards we have when playing the game. With different numbers of cards, our \_\_init__ function will choose different confidence designed for the game.

###### make_action
Function make_action is used to choose a new action depending on the current state of the game. This method implements our PokerBot strategy designed above. By using the state and round arguments, we can decide our next best move.
> __Parameters:__
> - __state:__ _ClientGameState_  
> The parameter _ClientGameState_ tracks the state object of the current game. A game consists of multiple rounds from deal to showdown.
> - __round:__ _ClientGameRoundState_  
> The parameter _ClientGameRoundState_ tracks the state object of the current round, from deal to showdown.

> __Returns:__
> - __Actions__ : _str, {'BET', 'CALL', 'CHECK', 'FOLD'} (and in round.get\_available\_actions())_
> A string representation of the next action an agent wants to do next, should be from a list of available actions.

###### on_image
Function on_image is called every time when the card image changes. Use this method for image recongition procedure.
> __Parameters:__
> - __image:__ _Image_  
> The parameter _image_ tracks the current Image object.

###### on_error
Function on_error will be called in case of error either from server backend or from client itself. It is easy to use this function for error handling, including logging and raising error.
> __Parameters:__
> - __error:__ _str_  
> The parameter _error_ records a string representation of the current error.

###### on_game_start
Function on_game_start will be called once at the beginning of the game when server confirms both players have connected. It will check whether .\log folder exists or not. If not then, it will make one. Meanwhile, it can initialize the conf and decay array.

###### on_new_round_request
Function on_new_round_request is called every time before a new round is started. A new round is started automatically.
> __Parameters:__
> - __state:__ _ClientGameState_  
> State object of the current game.

###### on_round_end
Funtion on_round_end is called every time a round has ended. A round ends automatically. It will log last round's result, if any, update current decay and log it.
> __Parameters:__
> - __state:__ _ClientGameState_  
> State object of the current game.
> - __round:__ _ClientGameRoundState_  
> State object of the current round.

###### on_game_end
Function on_game_end is called once after the game has ended. A game ends automatically and it will print the result of the game.
> __Parameters:__
> - __state:__ _ClientGameState_  
> State object of the current game.

> __Result:__ _str, {'WIN', 'DEFEAT'}_
> End result of the game.

###### __init_conf_decay
Function __init_conf_decay is called at game start to initialize conf and decay array according to the game type ['3', '4']. The array is in the order of ['J', 'Q', 'K', 'A'(if game type='4')]. Tune the numbers for Q and K to raise possibility to win.

###### __update_decay
Function __update_decay is called to update decay when every round ends. New values of decay depend on the last game's result and the last move.
> __Parameters:__
> - __outcome:__ _str_  
> The parameter _outcome_ records the result of the last game. 
> - __last_move:__ _str_  
> The parameter _last\_move_ records the last move.

---

## Project management
> Software project management is a sub-discipline of project management in which software projects are planned, implemented, monitored and controlled..[<sup>1</sup>](#refer-anchor-1)  

In this part, the planning, implementing, monitoring and controlling are introduced. The team is gathered by Detian Guo based on personal relationship and team member's availability.

### Project Planning
At the beginning of a project, the team identified the scope of the project, and split it to a set of tasks must be completed. Based on a naïve work load estimation, the team set up a project schedule as below.

![ ](.//doc_image//Plan_V1.png)

### Project Execution
The team is split to two sub teams. One focused on how to find and realize the strategy to win a Kuhn Poker game. The other one focused on find the best model for poker card identification. Plan was monitored and adjusted according to project status.

### Project Monitoring
The team scheduled a weekly meeting to check how did the plan went in the last week. Difficulties by achieving the best strategy and/or the best model were also discussed. The plan was adjusted according to real workload rather than estimated workload.

![ ](.//doc_image//Plan_V2.png)

### Project Control
The quality, time plan and risk of a project are the three primary elements to be managed for a project. In this assignment, our keen resource to manage is the available time of team members, which plays an important role on the three pillars mentioned above. This is achieved by the weekly meeting.

---

## Reference
<div id="refer-anchor-1"></div>
- [1][WikiPedia](https://en.wikipedia.org/wiki/Software_project_management)
