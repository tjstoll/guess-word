'''
Created: March 2016
Author: Taneisha Stoll

Guess Word. It's like Hangman but with a different name and no hanging man.
'''

# The randomizing algorithm uses the time the pick the word
from datetime import datetime as t

# Categories: Each index represents a level: 0: Easy, 1: Medium, 2: Hard
Animals = [['Dog', 'Cat', 'Monkey', 'Fish', 'Bird', 'Horse'], ['Gorilla', 'Faun', 'Elephant', 'Vulture', 'Cheetah', 'Alligator'], ['Dachshund', 'Orangutan', 'Komodo Dragon', 'Hugo', 'Tasmanian Devil', 'Pademelon']]
Food = [['Burger', 'Cake', 'Fries', 'Hot Dogs', 'Orange', 'Pizza'], ['Spaghetti', 'Ravioli', 'Fruit', 'Cereal', 'Rice Patty', 'Roti'], ['Squash', 'Steak', 'Nuggets', 'Shrimp Linguini Alfredo', 'Beef Bourguignon', 'Zucchini']]
Astro = [['Planet', 'Star', 'Sun', 'Photon', 'Atmosphere', 'Galaxy'], ['Andromeda', 'Lightyear', 'Constellation', 'Oort', 'Neutron Star', 'General Relativity'], ['Quarks', 'Exoplanet', 'Gamma Rays', 'Dark Matter', 'Hadron Collider', 'Black Body Radiation']]

# It's best to keep the categories and levels in libraries for easier access
Categories = {'Animals': Animals, 'Food': Food, 'Astro': Astro}
Levels = {'Easy': 0, 'Medium': 1, 'Hard':2}


def word_picker(cat_content, lev):
    '''
    Picks a word from cat_cont at level lev using a time based randomizing
    algorithm.
    
    >>> word_picker(Animals, Medium)
    'Faun'
    >>> word_picker(Animals, Medium)
    'Gorilla'
    '''
    
    # Sets up the random number to be used in finding a word
    date = str(t.now())
    ran_num = int(date[17:19])
    word_index = ((len(cat_content[lev])-0.1)/59)*ran_num

    return cat_content[lev][int(word_index)]

#===============================================================================

def solve(word):
        '''
        Solves the word to be guessed.
        
        >>> solve('Hadron Collider')
        H A D R O N 
        C O L L I D E R 
        >>> solve ('Star')
        S T A R 
        '''
        
        # Builds the solved line in the style of the gameboard
        displayed_line = 'The word was:\n'
        for i in range(len(word)):
            if word[i].isspace():
                displayed_line += '\n'
            else:
                displayed_line += '{} '.format(word[i].capitalize())

        return displayed_line

#===============================================================================

class GuessWord(object):
    '''
    GuessWord class controls game play and gameboard layout.
    '''

    def __init__(self, category, level):
        '''
        Initializes the information in the game based on category and level
        chosen by player and then calls for the game to be designed.
        '''
        
        word = word_picker(Categories[category], Levels[level])
        self.word = [word.upper(), len(word)]
        self.str_line = [[],'']
        self.strikes = 0
        self.letters_used = ''
        self.gameInfo = 'Category: {}\nLevel: {}\n'.format(category, level)
        
        self.build_line(True)
        
#===============================================================================
    
    def printInfo(self):
        '''
        Prints the information of the game.
        '''
        print('Letters Used: ', self.letters_used)
        print('Strikes: ', self.strikes)        
        print(self.gameInfo)
        
#===============================================================================

    def advance_game(self):
        '''
        Solves the game if maximum strikes are reached or once the player has
        correctly guessed all the letters within maximum strikes. Otherwise,
        the player is prompted to make another guess.
        '''
        
        # Checks that the player is under 10 strikes
        if self.strikes >= 10:
            self.printInfo()
            print("\nYOU'VE GOT {} STRIKES! YOU LOSE!\n".format(self.strikes))
            return solve(self.word[0])
        
        # Ends the game if all the right letters are guessed
        if ('_' not in self.str_line[0]) and\
           (int(len(self.str_line[0]))) == self.word[1]:            
            print('\nYOU WIN!')
            return solve(self.word[0])
        
        # Continues the game
        else:
            print('\n' + self.str_line[1] + '\n')
            self.printInfo()
            
            # Sets up the letter for mainpulation
            letter = input('Guess a letter or guess the word: ')
            let = letter.upper()
            
            return self.play_letter(let)        

#===============================================================================

    def build_line(self, initial=False, letter=''):
        '''
        Builds the initial gameboard if initial is True. Otherwise, updates
        gameboard with correct letter guessed.
        '''
        displayed_line = ''
        
        # Builds the initial gameboard
        if initial:
            for i in range(self.word[1]):
                if self.word[0][i].isspace():
                    self.str_line[0].append('\n')
                    displayed_line += '\n'
                    
                else:
                    self.str_line[0].append('_')
                    displayed_line += '_ '
                
        # Updates the gameboard with the new letter
        else:
            for i in range(self.word[1]):
                if self.word[0][i] == letter:
                    self.str_line[0][i] = '{}'.format(letter)

            for i in range(len(self.str_line[0])):
                if self.str_line[0][i] != '\n':
                    displayed_line += '{} '.format(self.str_line[0][i])
                else:
                    displayed_line += '\n'
                
        self.str_line[1] = displayed_line

        return self.advance_game()
        
#===============================================================================
    
    def play_letter(self, letter):
        '''
        Checks the input of the player and ends the game if letter is 'QUIT',
        letter is the word to be guessed. Advances the game if letter is in or
        not in word to be guessed or if letter has already been played.
        '''

        # Ends the game
        if len(letter) > 1:
            if letter == 'QUIT':
                self.strikes += 1000
                self.printInfo()
                print('BOO YOU QUITTER!')
                return solve(self.word[0])
            
            if letter == self.word[0]:
                self.printInfo()
                print("WOW THAT'S AMAZING! YOU WIN!")
                return solve(self.word[0])

            else:
                print('\n{} is not the word!'.format(letter))
                self.strikes += 3
                return self.advance_game()

        # Makes sure no letters get repeated
        if letter in self.letters_used:
            print("\nYou've already played the letter {}!".format(letter))
            return self.advance_game()

        # Checks whether the guess is correct or not
        elif len(letter) == 1:
            if letter in self.word[0]:
                self.letters_used += '{} '.format(letter)
                self.build_line(False, letter)

            else:
                self.strikes += 1
                self.letters_used += '{} '.format(letter)
                print('\nThere are no {}s in this word.'\
                      .format(letter.capitalize()))
                return self.advance_game()      

#===============================================================================

if __name__=='__main__':
    intro = "\n**************************** WELCOME TO GUESS WORD! ****************************\nPick a category, then pick a level, and then guess a letter or word to solve the\npuzzle. But wait! You only get 10 tries so choose wisely! And if you want to quit\nbecause you're a quitter then type the word 'quit' at any time.\nWould you like to play?\n"
    
    print(intro)

    category = input('Choose a category (Animals, Food, Astro): ')
    level = input('Choose a level (Easy, Medium, Hard): ')
        
    if category.lower() == 'quit' or level.lower() == 'quit':
        print('Bye Bye :)')
        pass
    else:
        g = GuessWord(category.capitalize(), level.capitalize())

