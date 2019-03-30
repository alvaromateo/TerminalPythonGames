'''
This is a script file that offers a terminal version of BlackJack game.
All rights reserved.
'''

# Imports

from os import system
from enum import Enum
from copy import deepcopy
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

# 'testMode' variable is for testing different game situations.
# It only works with 1 player!!
# 0 -> testing mode disabled. Normal game
# 1 -> split pairs
# 2 -> double down
# 3 -> player natural
# 4 -> player and dealer naturals
# 5 -> split and double down
testMode = 2

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
        if self.rank == 'Ace':
            return self.__get_ace_value__()
        return VALUES[self.rank]

    def set_hand(self, hand):
        self.hand = hand

    def __get_ace_value__(self):
        if self.hand.totalValue + 11 > BLACKJACK:
            return 1
        return 11

    def __str__(self):
        return self.rank + " " + self.suit
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.suit == other.suit and self.rank == other.rank

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
        self.discarded = []

    def __init_standard_deck__(self):
        standard_deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                standard_deck.append(card)
        return standard_deck

    def get_card(self):
        if not self.cards:
            print('Deck empty. Reshuffling...')
            self.shuffle_deck()
            print('Deck ready.')
        nextCard = self.cards.pop(0)
        self.discarded.append(nextCard)
        return nextCard

    def needs_shuffle(self):
        raise NotImplementedError("Abstract method. Subclasses must define it")

    def shuffle_deck(self):
        self.cards += self.discarded
        self.discarded = []
        shuffle(self.cards)
    
    def test_hand(self):
        self.shuffle_deck()
        # set the first cards in the same order as in 'testCards'
        for i, card in enumerate(testCards[testMode]):
            cardIndex = self.cards.index(card)
            self.cards[i], self.cards[cardIndex] = self.cards[cardIndex], self.cards[i]

class StandardDeck(Deck):
    '''
    Class that represents a standard Poker deck of 52 cards. The 'plastic mark' is always placed
    on top of the deck after each shuffling so that the cards are shuffled every time a new
    hand is going to be played.
    '''
    TOTAL_CARDS = Deck.CARDS_IN_DECK
    
    def __init__(self):
        Deck.__init__(self)
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
        self.plastic_mark = 0
        for _ in range(0, 6):
            self.cards += Deck.__init_standard_deck__(self)
        self.shuffle_deck()
    
    def get_card(self):
        self.plastic_mark -= 1
        return Deck.get_card(self)

    def needs_shuffle(self):
        return self.plastic_mark <= 0

    def shuffle_deck(self):
        Deck.shuffle_deck(self)
        self.plastic_mark = randint(int(SixPackDeck.TOTAL_CARDS * 0.8), SixPackDeck.TOTAL_CARDS)

class Hand():
    '''
    This class represents a hand of cards. It is initialized with 2 cards every round that is
    played. The two cards are drawn from the deck.
    '''
    def __init__(self, name = 'Hand'):
        self.__cards = []
        self.name = name
        self.totalValue = 0
        self.dirtyTotal = False
    
    def get_hand_value(self):
        if self.totalValue == 0 or self.dirtyTotal:
            valueWithoutAces = self.__get_hand_value_excluding_aces__()
            self.totalValue = valueWithoutAces + self.__get_aces_value__()
            self.dirtyTotal = False
        return self.totalValue
    
    def __get_aces_value__(self):
        aces = [card for card in self.__cards if card.rank == 'Ace']
        if self.totalValue == 0:
            if len(aces) == 0:
                return 0
            elif len(aces) == 1:
                return 11
            else:
                return 11 + len(aces) - 1
        else:
            acesValues = [ace.value() for ace in aces]
            return sum(acesValues)

    def __get_hand_value_excluding_aces__(self):
        cardValues = [card.value() for card in self.__cards if card.rank != 'Ace']
        return sum(cardValues)

    def add_card(self, deckOrCard):
        card = deckOrCard
        if isinstance(deckOrCard, Deck):
            card = deckOrCard.get_card()
        card.set_hand(self)
        self.__cards.append(card)
        self.dirtyTotal = True
    
    def get_cards(self):
        return self.__cards
    
    def can_split_pair(self):
        return len(self.__cards) == 2 and self.__cards[0] == self.__cards[1]
    
    def can_double_down(self):
        return len(self.__cards) == 2 and self.get_hand_value() >= 9 and self.get_hand_value() <= 11

    def split_hand(self, copiedObj = None):
        splitHand = copiedObj
        if self.can_split_pair():
            # if the copy is not done we do it here
            if splitHand is None:
                splitHand = deepcopy(self)
                splitHand.name = 'Split Hand'
            # delete the proper cards from each hand to make the split
            del splitHand.__cards[1]
            del self.__cards[0]
        return splitHand
    
    def is_natural(self):
        if len(self.__cards) >= 2:
            return self.__cards[0].value() + self.__cards[1].value() == BLACKJACK
        return False
    
    def get_starting_hand(self, deck):
        self.add_card(deck)
        self.add_card(deck)
    
    def get_full_hand_string(self):
        resultString = ''
        for card in Hand.get_cards(self):
            resultString = resultString + str(card) + '\n'
        return resultString[:-1]

    def __str__(self):
        return '{0}:\n'.format(self.name)

class DealerHand(Hand):
    '''
    This is the same as the Hand superclass but when printing it to the screen it hides the
    second card, which is the behavior for the Dealer hand.
    '''
    def __init__(self):
        Hand.__init__(self)
    
    def show_full_hand(self):
        print('Hand:')
        print(super().get_full_hand_string())

    def __str__(self):
        resultString = super().__str__()
        resultString += '[ HIDDEN ]\n'
        cards_except_first = Hand.get_cards(self)[1:]
        for card in cards_except_first:
            resultString = resultString + str(card) + '\n'
        return resultString[:-1]

class PlayerHand(Hand):
    '''
    This class adds a bet value to the hand.
    '''
    def __init__(self):
        Hand.__init__(self)
        self.bet = 0
        self.playable = True
    
    def __str__(self):
        resultString = super().__str__()
        resultString = 'Bet placed: {0}\n'.format(self.bet)
        return resultString + super().get_full_hand_string()

    def split_hand(self):
        splitHand = deepcopy(self)
        splitHand.name = 'Split Hand'
        return super().split_hand(splitHand)

class HandResult(Enum):
    DEALER_WINS = -1
    DRAW = 0
    PLAYER_WINS = 1
    PLAYER_NATURAL = 2

class Player():
    '''
    Class that represents a player of the game. It contains the amount of chips that the player
    has and the current hand in each of the rounds. 
    It contains the methods used to play the game like bet(), split()...
    '''
    def __init__(self, number, chips):
        self.name = "Player {0}".format(number)
        self.chips = chips
        self.hand = None
        self.splitHand = None
    
    def __str__(self):
        resultString = self.name + '\n'
        resultString += 'Chips remaining: {0}\n'.format(self.chips)
        if self.hand is not None:
            resultString += str(self.hand)
        if self.splitHand is not None:
            resultString = resultString + '\n' + str(self.splitHand)
        return resultString
    
    def __bet__(self, amount, handToBet):
        if self.chips < amount:
            raise PlayerError()
        self.chips -= amount
        handToBet.bet = amount

    def split_pair(self, deck):
        '''
        Let's the player choose if he/she wants to split pair.
        '''
        if self.hand is not None and self.hand.can_split_pair():
            # ask player if he/she wants to split pairs
            split = get_int("Split pairs? Yes(1) or No(0): ", filter_zero_one)
            if split and self.chips >= self.hand.bet:
                # create new hand
                self.splitHand = self.hand.split_hand()
                # update chips
                self.chips -= self.hand.bet
                # add card to each hand
                self.hand.add_card(deck)
                self.splitHand.add_card(deck)
                print(self.hand)
                print(self.splitHand)
    
    def double_down(self, handToDouble, deck):
        '''
        Let's the player choose if he/she wants to double down the bet.
        '''
        if handToDouble is not None and handToDouble.can_double_down():
            # ask player if he/she wants to double down the hand
            double = get_int("Double down {0}? Yes(1) or No(0): " \
                .format(handToDouble.name), filter_zero_one)
            if double and self.chips >= handToDouble.bet:
                self.chips -= handToDouble.bet
                handToDouble.bet *= 2
                handToDouble.add_card(deck)
                print(handToDouble)
                handToDouble.playable = False

    def hit_or_stay(self, hand, deck):
        '''
        This method allows the player to choose if he/she wants another card or prefers to stay.
        '''
        option = get_int('Hit(1) or Stay(0)? ', filter_zero_one)
        while option and hand.playable:
            hand.add_card(deck)
            print(hand)
            if hand.get_hand_value() < 21:
                option = get_int('Hit(1) or Stay(0)? ', filter_zero_one)
            else:
                hand.playable = False

    def compare_hands(self, dealer_hand, player_hand):
        '''
        This method compares the player hand to the dealer hand passed as parameter and returns 1 if
        the player's hand is better, 0 if they are tied and -1 if the dealer hand wins. 
        '''
        # first check natural Blackjack cases
        if dealer_hand.is_natural():
            if player_hand.is_natural():
                return HandResult.DRAW
            else:
                return HandResult.DEALER_WINS
        else:
            dealerVal = dealer_hand.get_hand_value()
            playerVal = player_hand.get_hand_value()
            # player hand natural and dealer not
            if player_hand.is_natural():
                return HandResult.PLAYER_NATURAL
            # player busted case
            elif playerVal > BLACKJACK:
                return HandResult.DEALER_WINS
            else:
                # dealer busted but player didn't
                if dealerVal > BLACKJACK:
                    return HandResult.PLAYER_WINS
                else:
                    # neither busted -> compare function: (a > b) - (a < b)
                    return HandResult((playerVal > dealerVal) - (playerVal < dealerVal))

    def payment(self, dealer_hand):
        '''
        This method checks the value bet by the player and adds the same value to the player's chips,
        but multiplied by result_multiplier.
        The result_multiplier parameter is the value returned by compare_hands. If the dealer won
        it will be -1, and the value will be substracted from the player chips. If the player won it will
        be 1 and the value will be added. Finally, if the match is a tie the result_multiplier will be
        0 and no addition or substraction will happen.
        '''
        # start play on hand(s)
        for hand in (self.hand, self.splitHand):
            if hand is not None:
                print(hand.name + ' -> Total: {0}'.format(hand.get_hand_value()))
                compareResult = self.compare_hands(dealer_hand, hand)
                if compareResult is HandResult.DEALER_WINS:
                    # player loses, nothing to do as we substract the chips when making the bet
                    print('You lose.')
                elif compareResult is HandResult.DRAW:
                    # draw, give back the chips
                    print('Draw')
                    self.chips += self.hand.bet
                    pass
                elif compareResult is HandResult.PLAYER_WINS:
                    # player wins, give back the bet x 2
                    print('You win!')
                    self.chips += self.hand.bet * 2
                    pass
                elif compareResult is HandResult.PLAYER_NATURAL:
                    # player natural, payment = bet x 2.5
                    print('BLACKJACK!')
                    self.chips += self.hand.bet * 2.5
                    pass

    def play(self, deck):
        # if player has a Blackjack return
        if self.hand.is_natural(): return
        # check if the player can and want to split pairs
        self.split_pair(deck)
        # check if the player can and want to double down on his hand
        self.double_down(self.hand, deck)
        # check if the player can and want to double down on his split hand
        self.double_down(self.splitHand, deck)

        # start play on hand(s)
        for hand in (self.hand, self.splitHand):
            if hand is not None and hand.playable:
                print(hand.name + ':')
                self.hit_or_stay(hand, deck)

    def new_hand(self, deck, min_bet, max_bet):
        print('Starting new hand')
        print(self.name + ':')

        if self.chips < min_bet:
            raise PlayerError()

        def bet_check(val):
            return val > 0 and val <= self.chips and val >= min_bet and val <= max_bet

        self.hand = PlayerHand()
        bet_to_place = get_int('How many chips do you want to bet? ', filter_positive_int)
        while not bet_check(bet_to_place):
            if bet_to_place > self.chips:
                print('You don\'t have that many chips.')
            else:
                print('Bet must be between {0} and {1} chips.'.format(min_bet, max_bet))
            bet_to_place = get_int('How many chips do you want to bet? ', filter_positive_int)

        self.__bet__(bet_to_place, self.hand)
        self.hand.get_starting_hand(deck)

class Dealer():
    '''
    Class to represent the dealer of the game. It contains the logic for the Dealer to play
    against the players. This is the same logic used in the casinos.
    '''
    def __init__(self):
        self.hand = None
    
    def play(self, deck):
        '''
        Dealer plays with the same rules always. If the card total is 16 points or lower,
        the dealer will always draw another card from the deck.
        '''
        while self.hand.get_hand_value() < 17 and not self.hand.get_hand_value() > BLACKJACK:
            newCard = deck.get_card()
            self.hand.add_card(newCard)
            print(newCard)
    
    def new_hand(self, deck):
        '''
        Starts a new hand for the dealer. The deck is passed by the Table.
        '''
        self.hand = DealerHand()
        self.hand.get_starting_hand(deck)
    
    def reveal_hand(self):
        '''
        Prints the hand of the dealer, including the hidden card.
        '''
        print('Dealer\n')
        self.hand.show_full_hand()

    def __str__(self):
        resultString = 'Dealer\n'
        resultString += str(self.hand)
        return resultString

class Table():
    '''
    This is the class that represents the game. It has the dealer and players objects, the
    deck with the cards and the logic to run the game.
    '''
    def __init__(self):
        # define variables
        self.deck = None
        self.players = []
        self.dealer = Dealer()
        # get options for table
        self.min_bet = get_int("Minimum bet: ", filter_positive_int)
        self.max_bet = get_int("Maximum bet: ", lambda num, min_bet = self.min_bet: num >= min_bet)
        self.deck_type = get_int("Deck type. Standard(0) or SixPack(1): ", filter_zero_one)
        self.num_players = get_int("Number of players: ", filter_positive_int)
        # init variables
        self.__init_deck__()
        self.__init_players__()

    def __init_deck__(self):
        if self.deck_type == 0:
            self.deck = StandardDeck()
        elif self.deck_type == 1:
            self.deck = SixPackDeck()

    def __init_players__(self):
        for index in range(0, self.num_players):
            print("Player {0}:".format(index))
            player_chips = get_int("How many chips do you want to buy? ", filter_positive_int)
            self.players.append(Player(index, player_chips))

    def __bets_payment__(self):
        for player in self.players:
            # clean screen
            system('clear')
            print('Dealer -> Total: {0}'.format(self.dealer.hand.get_hand_value()))
            print(player.name)
            player.payment(self.dealer.hand)
            input('\nPress any key to continue...')

    def __play_again__(self):
        # clean screen
        system('clear')
        current_players = {}
        for player in self.players:
            play = False
            print(player.name + ':')
            print('You have {0} chips remaining.'.format(player.chips))
            if player.chips < self.min_bet:
                print('You don\'t have enough chips to play.')
                input('\nPress any key to continue...')
            else:
                play = get_int("Another hand? Yes(1) or No(0): ", filter_zero_one)
            current_players[player] = play
        for (player, play) in current_players.items():
            if not play:
                self.players.remove(player)

    def __play_player_hand__(self, player):
        # clean screen
        system('clear')
        # show dealer hand
        print(self.dealer)
        print('')
        # show player hand
        print(player)
        print('')
        try:
            player.play(self.deck)
        except PlayerError:
            self.players.remove(player)
            print('Something went wrong. {0} kicked from game.'.format(player.name))
        input('\nPress any key to continue...')
    
    def __play_dealer_hand__(self):
        # clean screen
        system('clear')
        # show dealer hand
        self.dealer.reveal_hand()
        self.dealer.play(self.deck)
        input('\nPress any key to continue...')
    
    def play(self):
        while len(self.players) > 0:
            system('clear')
            # reshuffle the deck if needed
            if self.deck.needs_shuffle() or testMode != 0:
                if testMode == 0:
                    self.deck.shuffle_deck()
                else:
                    self.deck.test_hand()
            # init the hands of everyone in the table
            for player in self.players:
                try:
                    player.new_hand(self.deck, self.min_bet, self.max_bet)
                except PlayerError:
                    self.players.remove(player)
                    print('Something went wrong. {0} kicked from game.'.format(player.name))
            self.dealer.new_hand(self.deck)
            # begin game
            for player in self.players:
                self.__play_player_hand__(player)
            self.__play_dealer_hand__()
            # end game
            self.__bets_payment__()
            self.__play_again__()
        # no more players in table, so exit

class PlayerError(Exception):
    pass


# Global functions

def filter_zero_one(value):
    return value == 0 or value == 1

def filter_positive_int(value):
    return 0 < value

def get_int(message, filter_func=(lambda num: True), errMsg='Please, enter a valid value.'):
    '''
    This method gets and int, ensuring the value entered by the user is correct.
    '''
    value = -1
    filter_passed = False
    while(not filter_passed):
        value_str = input(message)
        try:
            value = int(value_str)
            filter_passed = filter_func(value)
        except ValueError:
            print(errMsg)

    return value

def start_game():
    '''
    This function initializes everything needed to play a game and starts it.
    It doesn't need any parameters and doesn't return anything.
    It is run if this script is run as '__main__'.
    '''
    system('clear')
    print('Welcome to Terminal Blackjack!')
    table = Table()
    table.play()
    print("See you soon!")
    # TODO: double down no funciona
    # TODO: cuando el jugador tiene natural y el dealer no, da draw. deberia ganar el jugador
    # TODO: test all testModes


testCards = {
    1: [
        Card('Hearts', '8'),
        Card('Diamonds', '8')
    ],
    2: [
        Card('Hearts', '6'),
        Card('Diamonds', '4')
    ],
    3: [
        Card('Hearts', 'Ace'),
        Card('Diamonds', 'King')
    ],
    4: [
        Card('Hearts', 'Ace'),
        Card('Diamonds', 'King'),
        Card('Spades', 'Ace'),
        Card('Clubs', 'Queen')
    ],
    5: [
        Card('Hearts', '8'),
        Card('Diamonds', '8'),
        Card('Spades', '2'),
        Card('Clubs', '3')
    ]
}

# Script call to main function

if __name__ == '__main__':
    start_game()
