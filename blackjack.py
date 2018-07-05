'''
This is a script file that offers a terminal version of BlackJack game.
All rights reserved.
'''

# Imports

from random import shuffle
from random import randint


# Global variables

# All suits of the standard deck
SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
# All cards in each suit of the standard deck
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
# Values for each of the cards in points
# Ace can be 11 or 1 but this is controlled through code
VALUES = {
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

BLACKJACK = 21


# Script classes

class Card():
    '''
    Class to represent cards. Each card has a string representation to be printed on the
    screen when playing the game. It also has a value in points.
    '''
    def __init__(self, suit, rank, hand=None):
        self.suit = suit
        self.rank = rank
        self.hand = hand
        
    def value(self):
        if rank == 'Ace':
            return self.__get_ace_value__()
        return values[self.rank]

    def set_hand(self, hand):
        self.hand = hand
        return hand.calculate_points(self.value())

    def __get_ace_value__(self):
        if self.hand.points() > BLACKJACK:
            return 1
        return 11

class Deck():
    '''
    Abstract class that provides the methods to be applied to the deck of cards that will
    be used during the game.
    The decks need to have cards and a 'plastic mark' that tells when a shuffling of the deck
    needs to be done (when the current hand has finished the deck is shuffled).
    There are to different types of decks depending on the type of game that the players want
    to play. See the classes that inherit from this one to know the differences in each of them.
    '''
    CARDS_IN_DECK = 52
    
    def __init__(self):
        self.cards = []

    def __init_standard_deck__(self):
        standard_deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                standard_deck.append(card)
        return standard_deck

    def get_card(self):
        return self.cards.pop(0)

    def needs_shuffle(self):
        raise NotImplementedError("Abstract method. Subclasses must define it")

    def shuffle_deck(self):
        shuffle(self.cards)

class StandardDeck(Deck):
    '''
    Class that represents a standard Poker deck of 52 cards. The 'plastic mark' is always placed
    on top of the deck after each shuffling so that the cards are shuffled every time a new
    hand is going to be played.
    '''
    TOTAL_CARDS = Deck.CARDS_IN_DECK
    
    def __init__(self):
        self.cards = Deck.__init_standard_deck__(self)

    def needs_shuffle(self):
        return True

class SixPackDeck(Deck):
    '''
    This class represents the game that is played in the casinos. Six card decks are shuffled
    together and the 'plastic mark' is placed randomly between the last 60 - 80 cards.
    '''
    NUM_DECKS = 6
    TOTAL_CARDS = Deck.CARDS_IN_DECK * NUM_DECKS
    
    def __init__(self):
        Deck.__init__(self)
        for i in range(0, 6):
            self.cards.append(Deck.__init_standard_deck__(self))
        self.shuffle_deck()
        
    def needs_shuffle(self):
        return length(self.cards) <= plastic_mark:

    def shuffle_deck(self):
        Deck.shuffle_deck(self)
        self.plastic_mark = randint(TOTAL_CARDS * 0.8, TOTAL_CARDS)

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

