# This file is responsible for initialising users by two ways: login or register.
# Thus, there are two main functions depending on users' response.
import json
from os.path import exists

# This function creates files for storing information about users, games and game's leaders.
# It checks if files exist or not. If they do not, function creates them.

def creatingFiles():

    if exists('usersGamesHistory.json') == False:
        with open('usersGamesHistory.json', 'w') as file:
            json.dump([], file, indent=2)

    if exists('usersLoginDetails.json') == False:
        with open('usersLoginDetails.json', 'w') as file:
            json.dump([], file, indent=2)

    if exists('leaderBoard.json') == False:
        with open('leaderBoard.json', 'w') as file:
            json.dump([], file, indent=2)

# This function requests the user whether they want to log in with an existing username and password or register.
# An exception is provided.
def initialisationOptions():
    initialisationOptionsReponse = input(('Would you like to log in(L) or register(R)? ')).lower()

    if initialisationOptionsReponse == 'r':
        return registration()
    if initialisationOptionsReponse == 'l':
        return login()
    if initialisationOptionsReponse != 'l' and initialisationOptionsReponse != 'r':
        print("\u001b[41mUnfortunately, I don't understand. Try again!\u001b[0m")
        return initialisationOptions()

# Function asks users whether they want to see password requirements  or not.
# An exception is provided.
def passwordRequirementsInstruction():
    passwordRequirements = input(
        'Would you like to see password requirements to successfully register? Yes or No: \n').lower()
    if passwordRequirements == 'yes':
        print('\u001b[35mPassword Requirements\u001b[0m:')
        print('| 1. It should be at least 6 characters.')
        print('| 2. Any upper letters should be included.')
        print('| 3. Spaces are not allowed.')
        print('| 4. At least one specific character (#, @, _, &) should be included.')
        print('| 5. At least one number should be included.\n')
    elif passwordRequirements == 'no':
        pass
    else:
        print("\u001b[41mSomething went wrong! Try again.\u001b[0m")
        passwordRequirementsInstruction()

# Registration function
# All exceptions are provided.
def registration():

    passwordRequirementsInstruction()
    username = input("Username: ")

    if ' ' in username:
        print('\u001b[Username should not consist of any spaces. Try again.\u001b[0m\n')
        return initialisationOptions()

    if bool(username.strip()) == False:
        print('\u001b[Username is blank. Try again.\u001b[0m\n')
        return initialisationOptions()

    with open('usersLoginDetails.json') as file:
        data = json.load(file)

    for item in data:
        if username == item['username']:
            print('\u001b[41mThis login is already used! Try a different one.\u001b[0m\n')
            return registration()

    password = input("Password: ")
    passwordConfirmation = input("Confirm your password: ")

    if password == passwordConfirmation:

        # Password checking: 1) Any upper letters should be included 2) It should not be blank
        # 3) Any spaces in password are not allowed 4) It should be at least 6 characters
        # 5) At least 1 number should be included 6) Specific characters (# or @ or  _ or &) should be included.
        if bool(password.strip()) == False:
            print('\u001b[41mPassword is blank. Try again.\u001b[0m\n')
            return initialisationOptions()

        if ' ' in password:
            print('\u001b[41mPassword should not consist of any spaces. Try again.\u001b[0m\n')
            return initialisationOptions()

        if len(password) < 6:
            print('\u001b[41mPassword should be at least 6 characters. Try again.\u001b[0m\n')
            return initialisationOptions()

        if any(item.isupper() for item in password) == False:
            print('\u001b[41mPassword does not consist of any upper letters. Try again.\u001b[0m\n')
            return initialisationOptions()

        if any(item.isdigit() for item in password) == False:
            print('\u001b[41mPassword should include at least 1 number. Try again.\u001b[0m\n')
            return initialisationOptions()

        if '#' not in password and '@' not in password and '_' not in password and '&' not in password:
            print('\u001b[41mPassword should include at least one specific character (# or @ or  _ or &). Try again.\u001b[0m\n')
            return initialisationOptions()

        userDetailsEntry = {"username": username, "password": password}
        userGameHistoryEntry = {'username': username, 'gamesNumber': 0, 'winnings': 0, 'losings': 0, 'draws': 0}

        # Storing all information into JSON files.
        with open('usersLoginDetails.json') as file:
           dataDetailsEntry = json.load(file)

        with open('leaderBoard.json') as file:
            leaderBoardEntry = json.load(file)

        dataDetailsEntry.append(userDetailsEntry)
        leaderBoardEntry.append(userGameHistoryEntry)

        with open('usersLoginDetails.json', 'w') as file:
            json.dump(dataDetailsEntry, file, indent=2)

        with open('leaderBoard.json', 'w') as file:
            json.dump(leaderBoardEntry, file, indent=2)

        print('\u001b[43mYou are successfully registered!\u001b[0m\n')
        return username


    else:
        print('\u001b[41mPasswords do not match. Try to register again.\u001b[0m')
        return initialisationOptions()

# Login function
# All exceptions are provided
def login():
    username = input("Username: ")
    password = input("Password: ")

    loginSign = False

    with open('usersLoginDetails.json') as file:
        data = json.load(file)

    # Checking if the user exists or not.
    for item in data:
        if username == item['username'] and password == item['password']:
            loginSign = True
            print('\u001b[43mYou have successfully logged in!\u001b[0m\n')
            return username

    if loginSign == False:
        print("\u001b[41mYour login or password are incorrect or you are not registered yet!\u001b[0m")
        return initialisationOptions()