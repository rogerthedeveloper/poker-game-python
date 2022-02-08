# Python 3.9

# Poker Game
from collections import Counter
import os
import random
from time import sleep
from colorama import Fore, Back, Style

# Card Class
class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def __eq__(self):
        return {
            "rank": self.rank,
            "suit": self.suit
        }

# Deck Class
class Deck:
    # List of cards
    def __init__(self):
        self.cards = []
        suits = ["Diamantes", "Treboles", "Corazones", "Espadas"]

        for suit in suits:
            for rank in range(1, 14):
                self.cards.append(Card(rank, suit))
    
    # shuflles the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # deals the top card
    def deal(self):
        return self.cards.pop()

    # deal flop cards
    def deal_flop(self):
        return [self.cards.pop(), self.cards.pop(), self.cards.pop()]

    # deal turn card
    def deal_turn(self):
        return self.cards.pop()

    # deal river card
    def deal_river(self):
        return self.cards.pop()

    # deck show cards
    def showCards(self, cards):
        for card in cards:

            rank = card.rank
            if card.rank == 1:
                rank = "A"
            elif card.rank == 11:
                rank = "J"
            elif card.rank == 12:
                rank = "Q"
            elif card.rank == 13:
                rank = "K"

            if card.suit == "Diamantes":
                print(Back.GREEN + Fore.RED + " " + str(rank) + " de " + card.suit  + " " + '♦' + " " + Style.RESET_ALL)

            elif card.suit == "Treboles":
                print(Back.GREEN + Fore.BLACK + " " + str(rank) + " de " + card.suit  + " " + '♣' + " "  + Style.RESET_ALL)
            
            elif card.suit == "Corazones":
                print(Back.GREEN + Fore.RED + " " + str(rank) + " de " + card.suit + " " + '♥' + " " + Style.RESET_ALL)

            elif card.suit == "Espadas":
                print(Back.GREEN + Fore.BLACK + " " + str(rank) + " de " + card.suit  + " " + '♠' + " " + Style.RESET_ALL)

# Player Class
class Player:
    def __init__(self, index):
        self.name = "Jugador " + str(index)
        self.balance = 500
        self.cards = []

    # player check
    def check(self):
        return 0

    # player call
    def call(self, amount):
        self.balance -= amount
        return amount

    # player bet
    def bet(self, amount):
        self.balance -= amount
        return amount

    # player fold
    def fold(self):
        return 0 

    # player raise
    def raiseBet(self, amount):
        self.balance -= amount
        return amount

    # player balance
    def getBalance(self):
        return self.balance

    # deal card
    def dealCard(self, card):
        self.cards.append(card)        

    # player show cards
    def showCards(self):
        for card in self.cards:

            rank = card.rank
            if card.rank == 1:
                rank = "A"
            elif card.rank == 11:
                rank = "J"
            elif card.rank == 12:
                rank = "Q"
            elif card.rank == 13:
                rank = "K"

            if card.suit == "Diamantes":
                print(Back.GREEN + Fore.RED + " " + str(rank) + " de " + card.suit  + " " + '♦' + " " + Style.RESET_ALL)

            elif card.suit == "Treboles":
                print(Back.GREEN + Fore.BLACK + " " + str(rank) + " de " + card.suit  + " " + '♣' + " "  + Style.RESET_ALL)
            
            elif card.suit == "Corazones":
                print(Back.GREEN + Fore.RED + " " + str(rank) + " de " + card.suit + " " + '♥' + " " + Style.RESET_ALL)

            elif card.suit == "Espadas":
                print(Back.GREEN + Fore.BLACK + " " + str(rank) + " de " + card.suit  + " " + '♠' + " " + Style.RESET_ALL)

    # player check hand
    def checkHand(self, community_cards):
        conmute_cards = self.cards + community_cards

        conmute_cards.sort(key=lambda x: x.rank)

        # check for three of a kind
        three_of_a_kind = self.checkThreeOfAKind(conmute_cards)
        if three_of_a_kind:
            return (4, three_of_a_kind)

        # check for double pair
        doublePair = self.checkDoublePair(conmute_cards)
        if doublePair:
            return (3, doublePair)

        # check for pair
        pair = self.checkPair(conmute_cards)
        if pair:
            return (2, pair)
        
        # check for high card
        high = self.checkHighCard(conmute_cards)
        if high:
            return (1, high)

    # check for three of a kind
    def checkThreeOfAKind(self, conmute_cards):
        cards = []
        for card in conmute_cards:
            cards.append(card.rank)

        group = Counter(cards).items()

        for item in group:
            if item[1] == 3:
                return (item[0])

    # check for double pair
    def checkDoublePair(self, conmute_cards):
        cards = []
        for card in conmute_cards:
            cards.append(card.rank)

        group = Counter(cards).items()

        pairs = []
        for item in group:
            if item[1] == 2:
                pairs.append(item[0])

            if len(pairs) == 2:
                return pairs

    # check for pair
    def checkPair(self, conmute_cards):
        cards = []
        for card in conmute_cards:
            cards.append(card.rank)

        group = Counter(cards).items()

        for item in group:
            if item[1] == 2:
                return (item[0])

    # check for high card
    def checkHighCard(self, conmute_cards):
        cards = []
        for card in conmute_cards:
            cards.append(card.rank)
        
        return max(cards)
            
# Game Class
class Game:

    # check for winner
    def checkWinner(self, players):
        hands = []

        for player in players:
            hands.append(player.checkHand(self.community_cards))

        #print(hands)
        bestHand = max(hands)
        handType = ""

        if bestHand[0] == 1:
            handType = "Carta alta"
        elif bestHand[0] == 2:
            handType = "Pareja"
        elif bestHand[0] == 3:
            handType = "Doble pareja"
        elif bestHand[0] == 4:
            handType = "Trio"

        rank = bestHand[1]
        if bestHand[1] == 1:
            rank = "A"
        elif bestHand[1]== 11:
            rank = "J"
        elif bestHand[1] == 12:
            rank = "Q"
        elif bestHand[1] == 13:
            rank = "K"

        winner = players[hands.index(max(hands))].name

        if  bestHand[0] == 3:
            print("Ganador: " + winner + ", con " + handType + " de " + str(rank[0]) + " y " + str(rank[1]))
        else:
            print("Ganador: " + winner + ", con " + handType + " de " + str(rank))

        sleep(5)

    # set the pot
    def setPot(self, amount):
        self.pot += amount

    # start a game
    def start(self):

        self.pot = 0.00
        self.community_cards = []
        self.players = []

        # clear console
        os.system('cls' if os.name == 'nt' else 'clear')

        self.deck = Deck()
        self.deck.shuffle()

        print(Fore.BLUE + "Iniciando un nuevo juego de Poker..." + Style.RESET_ALL)
        #sleep(1)

        print(Fore.GREEN + "Mezclando cartas..." + Style.RESET_ALL)
        #sleep(1)

        # print an empty line
        print()

        for i in range(4):
            self.players.append(Player(i+1))

        # deal 1st card to each player
        for player in self.players:
            player.dealCard(self.deck.deal())

        # deal 2nd card to each player
        for player in self.players:
            player.dealCard(self.deck.deal())

        # loop through players
        for i, player in enumerate(self.players):
            # clear console
            #os.system('cls' if os.name == 'nt' else 'clear')
            
            print(Fore.YELLOW + player.name + Style.RESET_ALL)
            player.showCards()

            # print an empty line
            print()

            # bets round
            

        # deal flop cards
        flop = self.deck.deal_flop()

        # show floop cards
        print("Flop: ")
        self.deck.showCards(flop)
        self.community_cards += flop

        # print an empty line
        print()

        # bets round

        # deal turn card
        turn = self.deck.deal_turn()

        # show turn card
        print("Turn: ")
        self.deck.showCards([turn])
        self.community_cards += [turn]

        # print an empty line
        print()

        # bets round

        # deal river card
        river = self.deck.deal_river()
        
        # show river card
        print("River: ")
        self.deck.showCards([river])
        self.community_cards += [river]

        # print an empty line
        print()

        # community cards
        print("Cartas comunitarias: ")
        self.deck.showCards(self.community_cards)

        # print an empty line
        print()

        # bets round

        # check players hands for a winner
        self.checkWinner(self.players)

# start the game   
game = Game()
game.start()

while(1):
    game.start()
