'''
This is a script file that offers a terminal version of BlackJack game.
All rights reserved.
'''

# Imports

import random


# Global variables

# All suits of the standard deck
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
# All cards in each suit of the standard deck
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
# Values for each of the cards in points
# Ace can be 11 or 1 but this is controlled through code
values = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11
}


# Script classes

class Card():
    '''
    Class to represent cards. Each card has a string representation to be printed on the
    screen when playing the game. It also has a value in points.
    '''
    pass

class Ace(Card):
    '''
    Aces are treated as a special object because their value will be calculated based on
    what's best for the player (it can be 1 or 11). All the other properties and methods
    are inherited from the Card class.
    '''
    pass

class Deck():
    '''
    Abstract class that provides the methods to be applied to the deck of cards that will
    be used during the game.
    The decks need to have cards and a 'plastic mark' that tells when a shuffling of the deck
    needs to be done (when the current hand has finished the deck is shuffled).
    There are to different types of decks depending on the type of game that the players want
    to play. See the classes that inherit from this one to know the differences in each of them.
    '''
    pass

class StandardDeck(Deck):
    '''
    Class that represents a standard Poker deck of 52 cards. The 'plastic mark' is always placed
    on top of the deck after each shuffling so that the cards are shuffled every time a new
    hand is going to be played.
    '''
    pass

class SixPackDeck(Deck):
    '''
    This class represents the game that is played in the casinos. Six card decks are shuffled
    together and the 'plastic mark' is placed randomly between the last 60 - 80 cards.
    '''
    pass

class Hand():
    '''
    This class represents a hand of cards. It is initialized with 2 cards every round that is
    played. The two cards are drawn from the deck.
    '''
    pass

class DealerHand(Hand):
    '''
    This is the same as the Hand superclass but when printing it to the screen it hides the
    second card, which is the behavior for the Dealer hand.
    '''
    pass

class Player():
    '''
    Class that represents a player of the game. It contains the amount of chips that the player
    has and the current hand in each of the rounds. 
    It contains the methods used to play the game like bet(), split()...
    '''
    pass

class Dealer():
    '''
    Class to represent the dealer of the game. It contains the logic for the Dealer to play
    against the players. This is the same logic used in the casinos.
    '''
    pass

class Table():
    '''
    This is the class that represents the game. It has the dealer and players objects, the
    deck with the cards and the logic to run the game.
    '''
    pass


# Global functions

def start_game():
    '''
    This function initializes everything needed to play a game and starts it.
    It doesn't need any parameters and doesn't return anything.
    It is run if this script is run as '__main__'.
    '''
    pass


# Script call to main function

if __name__ == '__main__':
    start_game()

