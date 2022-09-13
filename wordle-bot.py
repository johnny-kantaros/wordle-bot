# Version 2

import statistics 
import random


# Global variables




guess_hash = dict()
answer_hash = dict()
filler_hash = dict()
yellow_letters = []
green_letters = []





def playGame():

    print("\nWelcome to WordleBot 2.0!\n")

    #Preprocess

    global guess_hash
    global filler_hash
    global green_letters
    global yellow_letters


    # We will play the game as long as the user has not guessed the word and still has guesses left
    play_game = True
    guess_count = 0

    while play_game == True:

        if guess_count == 6:
            print("\nRan out of guesses! You lose!\n")
            play_game = False
            break

        else:


            guess_count += 1

            # Check if only one word left (User wins)
            
            if len(answer_hash) == 1: # Check if user won
                print("\nCongrats! The word was " + str(list(answer_hash)[0]) + "\nYou won in " + str(guess_count) + " guesses!\n")
                play_game = False
                
            

            elif len(answer_hash) == 0:
                print("No words left! Is it possible you typed the results incorrectly?")
                play_game = False
                break


            else: 
                
                if guess_count == 6:
                    print("\nCareful: Last Guess!")
                
                normalize()
                normalize_filler()

                print("Possible Words left: " + str(len(answer_hash)))

                choice = printChoice()

                if choice == '9':
                    play_game = False
                    break
            
                # Get guess

                guess = getGuess()

                # Once we have valid guess, we can then see how the user did

                result_dict, got_word = getResults()

                if got_word == True: # User guessed word right
                    print("\nCongrats! The word was " + str(list(answer_hash)[0]) + "\nYou won in " + str(guess_count) + " guesses!\n")
                    play_game = False


                interpretResults(result_dict, guess)
                




def interpretResults(result_dict, guess):


    duplicates = {}
    global yellow_letters
    global green_letters

    """
    Keep track of how many occurrences in word of each letter

    This method will be very helpful for examining duplicate scenarios

    """
    index = 0
    for letter in guess:

        if letter not in duplicates:

            # Create parent dict
            duplicates[letter] = {}

            if result_dict[index] == 'g':
                duplicates[letter]["g"] = 1
                duplicates[letter]["y"] = 0
                green_letters.append(letter)
            
            elif result_dict[index] == 'y':
                duplicates[letter]["y"] = 1
                duplicates[letter]["g"] = 0
                yellow_letters.append(letter)
            
            else:
                duplicates[letter]["y"] = 0
                duplicates[letter]["g"] = 0

        
        else:

            if result_dict[index] == 'g':
                duplicates[letter]["g"] += 1
                green_letters.append(letter)
            
            elif result_dict[index] == 'y':
                duplicates[letter]["y"] += 1
                yellow_letters.append(letter)

        index += 1



    # Need to narrow down words using results

    yellow = 0
    green = 0
    passed = 0
    count = 0

    # Use copy in order to make real time deletions
    for word, weight in guess_hash.copy().items():
        count += 1
    

        for index, result in result_dict.copy().items(): # iterate over result, compare to word

            # Green
            if result == 'g' and guess[index] != word[index]:
                del guess_hash[word]
                green += 1
                break

            # Yellow
            elif result == 'y':

                letter = guess[index]
                # three Scenarios:
                # if word doesnt contain the yellow letter, delete
                # if word has the yellow letter in same position, delete
                # if word has fewer letters than exist yellow duplicates (ex if 2 yellow e's), 
                #   but only one in word

                if guess[index] not in word or guess[index] == word[index]:
                    del guess_hash[word]
                    yellow += 1
                    break

                elif word.count(letter) < duplicates[letter]["y"]:
                    del guess_hash[word]
                    yellow += 1
                    break

            # Grey
            elif result == 'x':
                
                # In wordle bot 2.0, we are using our duplicates dict to manage grey letters
                # To accomplish, we simply examine the count of yellow + green in duplicates
                # if the examined word has a different number, delete word
                # Ex. no yellow or greens for "e", delete word if come across an e
                # However, if 1 yellow and 1 green "e", delete word if only 1 exists in word
                # Also delete if the examined word has the grey letter in same location

                letter = guess[index]
                total_occurrences = duplicates[letter]["g"] + duplicates[letter]["y"]

                if total_occurrences != word.count(letter):
                    del guess_hash[word]
                    passed +=1
                    break

                elif guess[index] == word[index]:
                    del guess_hash[word]
                    passed +=1
                    break


# FILLER


    # Need to narrow down words using results

    yellow = 0
    green = 0
    passed = 0
    count = 0

    # Use copy in order to make real time deletions
    for word, weight in filler_hash.copy().items():
        count += 1
    

        for index, result in result_dict.copy().items(): # iterate over result, compare to word

            

            # Grey
            if result == 'x':
                
                # For the filler word, we want to actually KEEP words with misaligned yellow and greens
                # in order to optimize the best possible filler word

                letter = guess[index]
                total_occurrences = duplicates[letter]["g"] + duplicates[letter]["y"]

                if total_occurrences != word.count(letter):
                    del filler_hash[word]
                    passed +=1
                    break

                elif guess[index] == word[index]:
                    del filler_hash[word]
                    passed +=1
                    break



# Answer Hash



    yellow = 0
    green = 0
    passed = 0
    count = 0

    # Use copy in order to make real time deletions
    for word, weight in answer_hash.copy().items():
        count += 1
    

        for index, result in result_dict.copy().items(): # iterate over result, compare to word

            # Green
            if result == 'g' and guess[index] != word[index]:
                del answer_hash[word]
                green += 1
                break

            # Yellow
            elif result == 'y':

                letter = guess[index]


                if guess[index] not in word or guess[index] == word[index]:
                    del answer_hash[word]
                    yellow += 1
                    break

                elif word.count(letter) < duplicates[letter]["y"]:
                    del answer_hash[word]
                    yellow += 1
                    break

            # Grey
            elif result == 'x':

                letter = guess[index]
                total_occurrences = duplicates[letter]["g"] + duplicates[letter]["y"]

                if total_occurrences != word.count(letter):
                    del answer_hash[word]
                    passed +=1
                    break

                elif guess[index] == word[index]:
                    del answer_hash[word]
                    passed +=1
                    break






def getResults():
    
    # This function is used for getting the results of a guess

    results = dict()
    index = 0
    got_word = True

    while index < 5:

        result = input("\nEnter result of position " + str(index+1) + "(g,y,x):\n")

        if result in ['g','y','x']:
            results[index] = result
            index += 1

            # Check if user got word

            if result == 'y' or result == 'x':
                got_word = False
        
        else:
            print("\nError: result must be g, y, or x\n")

    return results, got_word




def printChoice():

    # Helper function that prints out user-generated choice

    choice = getChoice()

    if choice == "1":
        print("\n" + str(list(guess_hash)[0]))

    elif choice == "2":
        
        if len(guess_hash) >= 5:
            print("\n")
            for i in range(5):
                print(str(list(guess_hash)[i]))
        
        else:
            for word, weight in guess_hash.items():
                print(word)


    elif choice == "3":
        
        if len(answer_hash) >= 5:
            print("\n")
            for i in range(5):
                print(str(list(answer_hash)[i]))
        
        else:
            for word, weight in answer_hash.items():
                print(word)


    elif choice == "4":
                
        for word, weight in guess_hash.items():
            print(word)

    elif choice == "5":
                
        for word, weight in answer_hash.items():
            print(word)


    elif choice == "6":

        rand_index = random.randint(0, len(guess_hash)-1)
        print("\n" + str(list(guess_hash)[rand_index]))

    elif choice =="7":
        if len(filler_hash) > 0:
            print("\n" + str(list(filler_hash)[0]))
        else:
            print("No Filler words at this time!")

    elif choice == "8":
        print("\n" + str(list(guess_hash)[len(guess_hash)-1]))

    elif choice == "9":
        print("Quitting . . . ")

    return choice







def getGuess():

    # Function to extract guess from user

    while True:

        guess = input("\nEnter Guess taken, or enter 'back' to return to main menu\n").upper()

        if guess.lower() == "back":

            printChoice()

        # Important to check if in dictionary

        elif guess in guess_hash or guess in filler_hash:
            return guess
        
        else:
            print("\nError: Guess not found in our Dictionary\n")

        

    
def getChoice():

    # Method to extract user choice for guessing

    while True:
        
        choice = input("\nChoose an option: \n\n0) Guess!\n1) Show optimal guess\n2) Show top 5 guesses\n3) Show top 5 possible answers\n4) Show all possible guesses\n5) Show all possible answers\n6) Random Guess\n7) Filler word\n8) Worst guess\n9) Quit\n")

        if choice in ["0","1","2","3","4","5","6", "7", "8", "9"]:
            return choice

        
        print("Error: Choose valid option!")




def readDict():

    global guess_hash # make hashtable have global scope
    global filler_hash
    global answer_hash
    
    with open("5LetterDictionary.txt", "r") as dictionary:

        # Will use words to optimize guesses / Narrow down list

        for word in dictionary:

            word = word.upper().replace("\n", "") # Get rid of whitespace

            guess_hash[word] = 0 # Store in hashtable for easy look up, stop here
            filler_hash[word] = 0


    with open("5_letter_possible_answers.txt", "r") as possible_words:

        # For each word, we need to evaluate its letter frequency and location 
        # in order to to perform statistical analysis

        for word in possible_words:

            word = word.upper().replace("\n", "") # Get rid of whitespace

            answer_hash[word] = 0 # Store in hashtable for easy look up, stop here

 
            
            
            
            
def getStats():

    # Letter_location Array: keep track of where letters appear most often in words
    # Letter_distribution Array: overall count of most common - appearing letters

    letter_location = [[0]*26 for i in range(5)]
    letter_distribution = [0]*26

    for word, weight in answer_hash.items():
            
        weight = 0 # Reset Weight
        index_of_word = 0 # Keep track of whrere in word we are
            
            
        for letter in word: # Iterate each letter
                
            char_index = ord(letter) - 65 # Use ASCII keys to index array
            letter_location[index_of_word][char_index] += 1

            letter_distribution[char_index] += 1 
            index_of_word += 1

    return letter_location, letter_distribution
    


def normalize():
    
    """
    In this method, we normalize our letter_location and letter_distribution values
    using Z-Scores. We then calculate "Weights" for each word by summing up the Z-Scores
    of their letter components. This ranking system will allow us to optimally guess on each
    turn during the game. The weight will be comprised of two components:

    1. The frequency of their letters
    2. The location of their letters
    
    """
    

    global guess_hash
    global answer_hash

    letter_location, letter_distribution = getStats()

    stdev_distribution = statistics.stdev(letter_distribution) # stdev of distribution
    mean_distribution = (len(answer_hash) * 5) / 26 # Mean for letter distribution

    # Create z-scores for distribution
    for i in range(len(letter_distribution)): 
        letter_distribution[i] = (letter_distribution[i] - mean_distribution) / stdev_distribution

    # Create z-scores for location
    for index in letter_location:

        stdev_location = statistics.stdev(index)
        mean_location = len(answer_hash) / 26

        for i in range(len(index)):
            
            index[i] = ((index[i] - mean_location) / stdev_location)


    # Now that we have Z-Scores, we can re-iterate through the words and assign weights

    for word, weight in answer_hash.items():

        index_of_word = 0
        prev_letters = dict()
        weight = 0

        
        for letter in word:

            char_index = ord(letter) - 65 # Get index
            
            if letter in prev_letters: # punish duplicates, bad guesses
                weight -= abs(letter_distribution[char_index] + letter_location[index_of_word][char_index])

            else:
                weight += letter_distribution[char_index] + letter_location[index_of_word][char_index]
            
            index_of_word += 1
            prev_letters[letter] = letter

        answer_hash[word] = weight
    


    # Sort dictionary by weight in Descending order for optimal guesses


    answer_hash = dict(sorted(answer_hash.items(), key=lambda item: item[1], reverse = True))



    # DO SAME FOR GUESS HASH


    for word, weight in guess_hash.items():

        index_of_word = 0
        prev_letters = dict()
        weight = 0

        
        for letter in word:

            char_index = ord(letter) - 65 # Get index
            
            if letter in prev_letters: # punish duplicates, bad guesses
                weight -= abs(letter_distribution[char_index] + letter_location[index_of_word][char_index])

            else:
                weight += letter_distribution[char_index] + letter_location[index_of_word][char_index]
            
            index_of_word += 1
            prev_letters[letter] = letter

        guess_hash[word] = weight
    


    # Sort dictionary by weight in Descending order for optimal guesses


    guess_hash = dict(sorted(guess_hash.items(), key=lambda item: item[1], reverse = True))




"""

FILLER METHODS

"""


def fillerStats():

    letter_location = [[0]*26 for i in range(5)]
    letter_distribution = [0]*26

    for word, weight in filler_hash.items():
            
        weight = 0 # Reset Weight
        index_of_word = 0 # Keep track of whrere in word we are
            
            
        for letter in word: # Iterate each letter
                
            char_index = ord(letter) - 65 # Use ASCII keys to index array
            letter_location[index_of_word][char_index] += 1

            letter_distribution[char_index] += 1 
            index_of_word += 1

    return letter_location, letter_distribution



def normalize_filler():

    global filler_hash
    global green_letters
    global yellow_letters

    letter_location, letter_distribution = fillerStats()

    stdev_distribution = statistics.stdev(letter_distribution) # stdev of distribution
    mean_distribution = (len(filler_hash) * 5) / 26 # Mean for letter distribution

    # Create z-scores for distribution
    for i in range(len(letter_distribution)): 
        letter_distribution[i] = (letter_distribution[i] - mean_distribution) / stdev_distribution

    # Create z-scores for location
    for index in letter_location:

        stdev_location = statistics.stdev(index)
        mean_location = len(filler_hash) / 26

        for i in range(len(index)):
            
            index[i] = ((index[i] - mean_location) / stdev_location)


    # Now that we have Z-Scores, we can re-iterate through the words and assign weights

    for word, weight in filler_hash.items():

        index_of_word = 0
        prev_letters = dict()
        weight = 0

        
        for letter in word:

            char_index = ord(letter) - 65 # Get index
            
            if letter in prev_letters: # punish duplicates, bad guesses
                weight -= abs(letter_distribution[char_index] + letter_location[index_of_word][char_index])
            
            elif letter in green_letters:
                weight -= 2* abs(letter_distribution[char_index] + letter_location[index_of_word][char_index])

            elif letter in yellow_letters:
                weight -= 2 * abs(letter_distribution[char_index] + letter_location[index_of_word][char_index])

            else:
                weight += letter_distribution[char_index] + letter_location[index_of_word][char_index]
            
            index_of_word += 1
            prev_letters[letter] = letter

        filler_hash[word] = weight
    


    # Sort dictionary by weight in Descending order for optimal guesses


    filler_hash = dict(sorted(filler_hash.items(), key=lambda item: item[1], reverse = True))

   
    

if __name__ == "__main__":
    readDict()
    playGame()

