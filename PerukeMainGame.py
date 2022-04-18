# Importing needed libraries
import random
import json
import time
import sys
# Connecting another function in other user initialisation file.
from userInitialisation import initialisationOptions, creatingFiles

# Initialising two players' disks
# True - protected. False - unprotected. None - attacked
player1 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
player2 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}


# Attacking function with initialising all possible outputs
def attack(player, turn, username1, username2, currentNumber, computerResponse):
    if player[currentNumber] == None:
        print('\u001b[41mThis disk is already attacked!\u001b[0m\n')
        noChoice(turn, username1, username2, currentNumber, computerResponse)

    if player[currentNumber] == False:
        player[currentNumber] = None

    if player[currentNumber] == True:
        player[currentNumber] = False


# Protecting function with initialising all possible outputs
def protect(player, turn, username1, username2, currentNumber, computerResponse):
    if player[currentNumber] == True:
        print("\u001b[41mThis disk is already protected.\u001b[0m\n")
        noChoice(turn, username1, username2, currentNumber, computerResponse)

    if player[currentNumber] == None:
        print('\u001b[41mThis disk is impossible to protect.\u001b[0m\n')
        noChoice(turn, username1, username2, currentNumber, computerResponse)

    if player[currentNumber] == False:
        player[currentNumber] = True


# This function checks if there are no possible actions or choices to attack or protect.
# If there are no actions -> next dice move
def noChoice(turn, username1, username2, currentNumber, computerResponse):
    if turn == None:
        gettingUserResponseOnePlayerGame(username1, username2, currentNumber, computerResponse)
    else:
        gettingUserResponse(turn, username1, username2, currentNumber)


# This function requests two possible outcomes from the user: whether attack or protect one's disk.
# After getting the decision from the user, function redirects to two functions with attacking and protecting content above.
# All exceptions are provided
def gettingUserResponse(turn, username1, username2, currentNumber):
    if turn == True or turn == None:
        print(f'This is {username1}"s turn! Please choose whether attack or protect your disk: A or P.')
    else:
        print(f"This is {username2}'s turn! Please choose whether attack or protect your disk: A or P.")
    userResponse = input("Player's choice: ").lower()

    computerResponse = None

    if userResponse == "a":
        if (turn == True or turn == None):
            attack(player2, turn, username1, username2, currentNumber, computerResponse)
        else:
            attack(player1, turn, username1, username2, currentNumber, computerResponse)

    if userResponse == "p":
        if (turn == True or turn == None):
            protect(player1, turn, username1, username2, currentNumber, computerResponse)
        else:
            protect(player2, turn, username1, username2, currentNumber, computerResponse)

    if ((userResponse != "a") and (userResponse != "p")):
        print("\u001b[41mSomething went wrong! Try again.\u001b[0m")
        gettingUserResponse(turn, username1, username2, currentNumber)


# This function prints players' disks dashboard. The reason why it is needed to create an individual function is based
# on the nature of colours in the python terminal. It works only with strings rather than dictionaries or lists.
def diskBoardForPrint(player, username1, username2):
    outputString = ''
    for counter in player:
        if player[counter] == True:
            outputString = outputString + str(counter) + '.\u001b[32mTrue \u001b[0m'
        if player[counter] == False:
            outputString = outputString + str(counter) + '.\u001b[31mFalse \u001b[0m'
        if player[counter] == None:
            outputString = outputString + str(counter) + '.\u001b[30mNone \u001b[0m'

    if player == player1:
        print(f'\u001b[4m\u001b[1m{username1}\u001b[0m:', outputString)
    if player == player2:
        print(f'\u001b[4m\u001b[1m{username2}\u001b[0m:', outputString, '\n')


# This function inserts the data about the game into a JSON file called "usersGamesHistory.json"
def userGamesHistoryInserting(userGamesHistoryEntry):
    with open('usersGamesHistory.json') as file:
        dataGamesHistory = json.load(file)

    dataGamesHistory.append(userGamesHistoryEntry)

    with open('usersGamesHistory.json', 'w') as file:
        json.dump(dataGamesHistory, file, indent=2)


# Function stands for scoring, collecting and putting these values into JSON files.
def score(username1, username2, numberOfRounds, turn):
    from datetime import datetime
    score1 = 0
    score2 = 0
    datetime = datetime.now()

    # Calculating the actual players score.
    for counter in range(1, 7):
        if player1[counter] == True:
            score1 += 3
        if player1[counter] == False:
            score1 += 1

    for counter in range(1, 7):
        if player2[counter] == True:
            score2 += 3
        if player2[counter] == False:
            score2 += 1

    print(f"{username1}'s score:", score1)
    print(f"{username2}'s score:", score2)

    with open('usersGamesHistory.json') as file:
        dataGamesHistory = json.load(file)

    # Comparing two scores to find the winner, loser. If score1 = score2, there is a draw.
    if score1 == score2:
        print("\u001b[43;1mThere is a draw!\u001b[0m")
        winnerEntry = None
        loserEntry = None
        drawEntry = True

    if score1 > score2:
        if turn == None:
            print(f"\u001b[43;1m{username1} is a winner!\u001b[0m")
        else:
            print(f"\u001b[43;1m{username1} is a winner! Congratulations!\u001b[0m")
        winnerEntry = username1
        loserEntry = username2
        drawEntry = False

    if score1 < score2:
        print(f"\u001b[43;1m{username2} is a winner! Congratulations!\u001b[0m")
        winnerEntry = username2
        loserEntry = username1
        drawEntry = False

    # Initialising the game type
    gameType = 'twoPlayersGame'
    if username2 == 'VirtualPlayer':
        gameType = 'onePlayerGame'

    # Forming the entry for storing information into Game History File.
    gameHistoryEntry = {
        'info': {'dateAndTime': str(datetime), 'gameIndex': len(dataGamesHistory) + 1,
                 'numberOfRounds': numberOfRounds,
                 'gameType': gameType}, 'winner': winnerEntry, 'loser': loserEntry, 'draw': drawEntry,
        'diskBoard': {
            f'{username1}': player1, f'{username2}': player2}}
    userGamesHistoryInserting(gameHistoryEntry)

    # Leader Board stands for the numerical indicators of wins, losses and draws for a certain player.
    # Process of putting information into a JSON file:
    # 1) Load an existed json file with and consider the content within the file as a list
    # 2) Append new content into a list
    # 3) Dump or upload the information into a file.
    with open('leaderBoard.json') as file:
        leaderBoardData = json.load(file)

    for item in leaderBoardData:
        if username1 == item['username'] and winnerEntry == username1:
            item['winnings'] += 1
            item['numberOfGames'] += 1
        if username2 == item['username'] and winnerEntry == username2:
            item['winnings'] += 1
            item['numberOfGames'] += 1
        if username1 == item['username'] and loserEntry == username1:
            item['losings'] += 1
            item['numberOfGames'] += 1
        if username2 == item['username'] and loserEntry == username2:
            item['losings'] += 1
            item['numberOfGames'] += 1
        if (username1 == item['username'] or username2 == item['username']) and drawEntry == True:
            item['numberOfGames'] += 1
            item['draws'] += 1

    with open('leaderBoard.json', 'w') as file:
        json.dump(leaderBoardData, file, indent=2)
    print('All information is successfully stored!\n')


# This class works after the game and may be called to show game statistics of players
def playersStatisticsRequest(username1, username2):
    with open('leaderBoard.json') as file:
        playersStatisticsData = json.load(file)

    for item in playersStatisticsData:

        if username1 == item['username']:
            print('')
            print(f'\u001b[1m\u001b[4mGames Statistics History for \u001b[33;1m{username1}\u001b[0m:')
            print(f'You have played {item["numberOfGames"]} game(s) in total.')
            print(f'You won {item["winnings"]} time(s).')
            print(f'You lost {item["losings"]} time(s).')
            print(f'You had a draw {item["draws"]} time(s).\n')

        if username2 == item['username']:
            print('')
            print(f'\u001b[1m\u001b[4mGames Statistics History for \u001b[33;1m{username2}\u001b[0m:')
            print(f'You have played {item["numberOfGames"]} game(s) in total.')
            print(f'You won {item["winnings"]} time(s).')
            print(f'You lost {item["losings"]} time(s).')
            print(f'You had a draw {item["draws"]} time(s).')


# Main part of multiple players game mode. The central for loop goes until number of rounds are reached.
# It calls other functions of the code.
def twoPlayersGame():
    # Variable turn stands for the players' turn.
    # If turn is True, there is a player's 1 turn. False -> Player's 2 turn. None -> No turn as there is single mode.
    turn = True
    identicalPlayersCheck = False

    # Checking if users are the same. Entering logins until they are different
    while identicalPlayersCheck == False:

        print('\u001b[1mPlease, complete the login or registration form for Player 1:\u001b[0m')
        username1 = initialisationOptions()

        print('\u001b[1mPlease, complete the login or registration form for Player 2:\u001b[0m')
        username2 = initialisationOptions()

        if username1 != username2:
            identicalPlayersCheck = True
        else:
            print('\u001b[41mPlayers are the same :) Try to login or register once again.\u001b[0m\n')

    # An exception is provided of the input is provided.
    while True:
        try:
            numberOfRounds = int(input("How many rounds do you want to play?\n"))
            if type(numberOfRounds) == int:
                break
        except:
            print('\u001b[41mYour response is incorrect. Try again :)\u001b[0m ')

    if numberOfRounds % 2 == 1:
        print(
            f'\u001b[35mYou need to play an even number of rounds. You will play {numberOfRounds + 1} rounds. \u001b[0m\n')
        numberOfRounds += 1

    # Main loop where functions are called.
    for counter in range(1, numberOfRounds + 1):
        currentNumber = random.randint(1, 6)
        print(f'\u001b[44;1mRound number {counter}.\u001b[0m')
        print(f"Dice shows number \u001b[33;1m{currentNumber}\u001b[0m")

        # The program gives different answers depending on the player whose turn it is to walk
        if turn == True:
            if (player1[currentNumber] == True or player1[currentNumber] == None) and player2[currentNumber] == None:
                print(f"This is {username1}'s turn! Please choose whether attack or protect your disk: A or P.")
                print('\u001b[41mThere are no possible actions with this dice!\u001b[0m\n')
            else:
                gettingUserResponse(turn, username1, username2, currentNumber)

        if turn == False:
            if (player2[currentNumber] == True or player2[currentNumber] == None) and player1[currentNumber] == None:
                print(f"This is {username2}'s turn! Please choose whether attack or protect your disk: A or P.")
                print('\u001b[41mThere are no possible actions with this dice!\u001b[0m\n')
            else:
                gettingUserResponse(turn, username1, username2, currentNumber)

        # Outputting current disks dashboard
        diskBoardForPrint(player1, username1, username2)
        diskBoardForPrint(player2, username1, username2)

        # Move transition
        turn = not turn

    # Two functions in the end of the game work to store, calculate the information about game results as well as
    # asking users to get a statistics of the game.
    score(username1, username2, numberOfRounds, turn)
    statisticsQuestion(username1, username2)


# Function outputs the loading message for the Virtual Player turn.
def loadingAnimation():
    for i in range(random.randint(3, 9)):
        sys.stdout.write('\rLoading...')
        time.sleep(0.1)
        sys.stdout.write('\rLoading..')
        time.sleep(0.1)
        sys.stdout.write('\rLoading.')
        time.sleep(0.1)
    sys.stdout.write('\rDone!      \n')


# Main part of single player game mode.
def onePlayerGame():
    print('\u001b[1mPlease, complete the login or registration form:\u001b[0m')
    username1 = initialisationOptions()
    username2 = 'VirtualPlayer'

    # Computer randomly chooses whether attack or protect:
    computerChoices = ('a', 'p')
    turn = None

    # An exception is provided.
    while True:
        try:
            numberOfRounds = int(input("How many rounds do you want to play?\n"))
            if type(numberOfRounds) == int:
                break
        except:
            print('\u001b[41mYour response is incorrect. Try again :)\u001b[0m')

    # It is important to check if there is an even number of rounds or not.
    # If it is not, just warn users about this changing
    if numberOfRounds <= 0:
        print(f'\u001b[35mYou need to play a positive number of rounds. \u001b[0m\n')
        return onePlayerGame()

    if numberOfRounds % 2 == 1:
        print(
            f'\u001b[35mYou need to play an even number of rounds. You will play {numberOfRounds + 1} rounds. \u001b[0m\n')
        numberOfRounds += 1

    for counter in range(1, numberOfRounds + 1, 2):
        currentNumber = random.randint(1, 6)
        print(f'\u001b[44;1mRound number {counter}.\u001b[0m')
        print(f"Dice shows number \u001b[33;1m{currentNumber}\u001b[0m")

        computerResponse = random.choice(computerChoices)

        if (player1[currentNumber] == True or player1[currentNumber] == None) and player2[currentNumber] == None:
            print(f"This is {username1}'s turn! Please choose whether attack or protect your disk: A or P.")
            print('\u001b[41mThere are no possible actions with this dice!\u001b[0m\n')
        else:
            gettingUserResponseOnePlayerGame(username1, username2, currentNumber, computerResponse)

        diskBoardForPrint(player1, username1, username2)
        diskBoardForPrint(player2, username1, username2)

        currentNumber = random.randint(1, 6)
        print(f'\u001b[44;1mRound number {counter + 1}.\u001b[0m')
        print(f"Dice shows number \u001b[33;1m{currentNumber}\u001b[0m")

        loadingAnimation()

        # Checking all possibilities for the computer to interact with the real player's disks.
        if (player2[currentNumber] == True or player2[currentNumber] == None) and player1[currentNumber] == None:
            print('\u001b[41mThere are no possible actions with this dice!\u001b[0m\n')
        else:
            if computerResponse == 'a':
                if player1[currentNumber] == None:
                    print('Virtual Player chooses to protect its own disk')
                    protect(player2, turn, username1, username2, currentNumber, computerResponse)
                else:
                    print('Virtual Player chooses to attack your disk')
                    attack(player1, turn, username1, username2, currentNumber, computerResponse)
            if computerResponse == 'p':
                if player2[currentNumber] == None or player2[currentNumber] == True:
                    print('Virtual Player chooses to attack your disk')
                    attack(player1, turn, username1, username2, currentNumber, computerResponse)
                else:
                    print('Virtual Player chooses to protect its own disk')
                    protect(player2, turn, username1, username2, currentNumber, computerResponse)

        diskBoardForPrint(player1, username1, username2)
        diskBoardForPrint(player2, username1, username2)
        time.sleep(1.5)

    score(username1, username2, numberOfRounds, turn)
    statisticsQuestion(username1, username2 = False)  # There is no player 2 as there is a virtual player.


# Function provides a question for the user to give the one's games statistics or not.
# An exception is provided.
def statisticsQuestion(username1, username2):
    whetherYesOrNotStats = input(
        '\u001b[35mWould you like to see your games statistics history: Yes or No?\u001b[0m \n').lower()
    if whetherYesOrNotStats == 'yes':
        playersStatisticsRequest(username1, username2)
        playAgain()
    elif whetherYesOrNotStats == 'no':
        playAgain()
    else:
        print("\u001b[41mSomething went wrong. Try again.\u001b[0m\n")
        statisticsQuestion(username1, username2)


# As well as gettingUserResponse function at the beginning of the code, function asks user to decide whether attack or protect the disk
# The only difference is that the function does not indicate the nickname of the player, since only one player is playing
def gettingUserResponseOnePlayerGame(onePlayerGameUsername, computerUsername, currentNumber, computerResponse):
    oneUserResponse = input('Please choose whether attack or protect your disk: A or P: ').lower()
    turn = None
    if oneUserResponse == 'a':
        attack(player2, turn, onePlayerGameUsername, computerUsername, currentNumber, computerResponse)
    if oneUserResponse == 'p':
        protect(player1, turn, onePlayerGameUsername, computerUsername, currentNumber, computerResponse)
    if ((oneUserResponse != "a") and (oneUserResponse != "p")):
        print("\u001b[41mSomething went wrong! Try again.\u001b[0m")
        gettingUserResponseOnePlayerGame(onePlayerGameUsername, computerUsername, currentNumber, computerResponse)


# Greeting function. Initial message after running the game
def greeting():
    print('----------------------------------------------------------------------------------------------')
    print(
        '***************************** \u001b[35mHello! Welcome to the Peruke Game\u001b[0m ******************************')
    print(
        '*** \u001b[35mIt is created in terms of Computer Science Python Project at the University of Warwick\u001b[0m *** ')
    print(
        '********* \u001b[35mMore detailed rules and description of the program can be found in GitHub:\u001b[0m ********* ')
    print('*************************** https://github.com/mionitsa/PerukeGame ***************************')
    print(
        '*********************** \u001b[35mProgram was created by Michael Ionitsa in 2022\u001b[0m *********************** ')
    print(
        '******************************  \u001b[35mEnjoy playing this Peruke Game!\u001b[0m ******************************')
    print('----------------------------------------------------------------------------------------------\n')

    creatingFiles()
    gameTypeResponse()


# Initialising a game type that user wants to play.
# An exception is provided.
def gameTypeResponse():
    gameType = input('\u001b[35mWould you like to play with your friend (F) or with virtual player (V)?\u001b[0m\n').lower()
    if gameType == 'f':
        twoPlayersGame()

    if gameType == "v":
        onePlayerGame()

    if gameType != "f" and gameType != "v":
        print('\u001b[41mSomething went wrong. Try to answer the question again.\u001b[0m')
        gameTypeResponse()

# The program does not stop after one game is done. Users are able to choose whether they want to play one more game or not.
def playAgain():
    playAgainResponse = input('\u001b[35mWould you like to play again: Yes or No? \u001b[0m').lower()

    if playAgainResponse == 'yes':
        global player1
        global player2
        player1 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
        player2 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
        gameTypeResponse()
    elif playAgainResponse == 'no':
        print('\u001b[35mThank you for playing the Peruke Game! See you later!\u001b[0m')
    else:
        print('\u001b[41mSomething went wrong. Try to answer the question again.\u001b[0m')
        playAgain()


# Running the initial greeting function in order to start the game process
greeting()
