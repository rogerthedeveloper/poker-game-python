# Python 3.9

# Poker Game
from collections import Counter
import os
import random
from time import sleep
from colorama import Fore, Back, Style
import pygame

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

    # player balance
    def getBalance(self):
        return self.balance

    # deal card
    def dealCard(self, card):
        self.cards.append(card) 

    # clear player cards
    def clearCards(self):
        self.cards = []
           

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

    def getVersion(self):
        return "0.0.1"

    def welcome(self):
        print(Fore.GREEN + """
 _____      _              
|  __ \    | |             
| |__) |__ | | _____ _ __  
|  ___/ _ \| |/ / _ \ '__| 
| |  | (_) |   <  __/ |    
|_|   \___/|_|\_\___|_|    
""")
        print("@rogerfsosa   Versión: " + self.getVersion())
        print("============================" + Style.RESET_ALL)

    def init(self):

        self.players = []

        # create players
        nPlayers = input("Número de jugadores (2 - 8): ")
        # print an empty line
        print()
        if nPlayers:
            nPlayers = int(nPlayers)
            if nPlayers >= 2 and nPlayers <= 8:
                for i in range(nPlayers):
                    tmpPlayer = Player(i+1)
                    tmpPlayer.id = i+1
                    tmpName = input("Nombre del jugador " + str(i+1) + ": ")
                    if tmpName:
                        tmpPlayer.name = tmpName
                    self.players.append(tmpPlayer)
                    self.dealer = 0
            else:
                print(Fore.RED + "Número de jugadores debe ser entre 1 y 8\n" + Style.RESET_ALL)
                self.init()
        else:
            print(Fore.RED + "Número de jugadores debe ser entre 1 y 8\n" + Style.RESET_ALL)
            self.init()

        # print an empty line
        print()
        
        # ask for small blind
        tmpSmallBlind = input("Ciega pequeña: Q")
        if tmpSmallBlind:
            tmpSmallBlind = int(tmpSmallBlind)
            if tmpSmallBlind > 0 and tmpSmallBlind <= self.players[0].getBalance():
                self.smallBlind = tmpSmallBlind

        # ask for big blind
        tmpBigBlind = input("Ciega grande: Q")
        if tmpBigBlind:
            tmpBigBlind = int(tmpBigBlind)
            if tmpBigBlind > 0 and tmpBigBlind > tmpSmallBlind and tmpBigBlind <= self.players[0].getBalance():
                self.bigBlind = tmpBigBlind
            
    # set dealer player
    def setDealer(self):
        if self.dealer < len(self.players):
            self.dealer = self.dealer+1
        else:
            self.dealer = 1
              
    # blinds turn
    def blindTurn(self, player):
        print("1. Ir\n2. No ir\n3. Subir")
        opt = input("Opción: ")

        if opt == "1":
            self.pot += player.bet(self.bigBlind)

        if opt == "2":
            player.fold()

        elif opt == "3":
            self.pot += player.bet(self.bigBlind * 2)

    # bets turn
    def betsTurn(self, player):
        print("1. Pasar\n2. Subir\n3. Rendirse")
        opt = input("Opción: ")

        if opt == "1":
            player.check()

        if opt == "2":
            self.pot += player.bet(self.smallBlind * 2)

        elif opt == "3":
            player.fold()

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

        winner = players[hands.index(max(hands))]

        if  bestHand[0] == 3:
            print("Ganador: " + winner.name + ", con " + handType + " de " + str(rank[0]) + " y " + str(rank[1]))
        else:
            print("Ganador: " + winner.name + ", con " + handType + " de " + str(rank))

        # print an empty line
        print()

        # winner player cards
        print(Fore.YELLOW + "Cartas / " + winner.name + Style.RESET_ALL + " - " + "Q" + str(winner.balance))
        winner.showCards()

        # print an empty line
        print()

        # win the pot
        winner.balance += self.pot

        print(winner.name + " gana el bote de: " + "Q" + str(self.pot))

        # print an empty line
        print()

        input(Fore.YELLOW + "Presione enter para iniciar un nuevo juego o esc para salir..." + Style.RESET_ALL)
        
    # set the pot
    def setPot(self, amount):
        self.pot += amount

    # start a game
    def start(self):

        self.pot = 0
        self.community_cards = []
        self.bigBlind = self.smallBlind * 2
        self.setDealer()

        # clear console
        os.system('cls' if os.name == 'nt' else 'clear')

        # welcome message
        self.welcome()

        self.deck = Deck()
        self.deck.shuffle()

        print(Fore.BLUE + "Iniciando un nuevo juego de Poker..." + Style.RESET_ALL)
        sleep(1)

        # print an empty line
        print()

        print(Fore.GREEN + "Mezclando cartas..." + Style.RESET_ALL)
        sleep(1)

        # print an empty line
        print()

        # deal 1st card to each player
        for player in self.players:
            player.dealCard(self.deck.deal())

        # deal 2nd card to each player
        for player in self.players:
            player.dealCard(self.deck.deal())

        # order players starting from dealer position
        self.players.sort(key=lambda x: x.id == self.dealer, reverse=False)
        
        # loop through players
        for i, player in enumerate(self.players):

            # clear console
            os.system('cls' if os.name == 'nt' else 'clear')

            # welcome message
            self.welcome()

            # pot balance
            print("Bote: " + "Q" + str(self.pot))

            # blinds
            print("Ciegas: " + "Q" + str(self.smallBlind) + " / " + "Q" + str(self.bigBlind))
            # print an empty line
            print()

            if i == 0:
                # show who is the dealer
                print(Fore.BLUE + self.players[-1].name + ", eres el dealer" + Style.RESET_ALL)

                # print an empty line
                print()
            elif i < (len(self.players) - 1):
                # show who is the dealer
                print(Fore.BLUE + self.players[-1].name + ", es el dealer" + Style.RESET_ALL)

                # print an empty line
                print()

            # turn of next player
            input(Fore.GREEN + "Turno de " + player.name + ", presiona enter..." + Style.RESET_ALL)

            # print an empty line
            print()

            print(Fore.YELLOW + "Cartas / " + player.name + Style.RESET_ALL + " - " + "Q" + str(player.balance))
            player.showCards()

            # print an empty line
            print()

            # show if is small blind
            if i == 0:
                print(Fore.BLUE + player.name + ", eres la ciega pequeña: Q" + str(self.smallBlind) + Style.RESET_ALL)              
                
                # print an empty line
                print()

                # small blind msg
                input(Fore.GREEN + "Presiona enter para colocar la ciega pequeña..." + Style.RESET_ALL)
                self.pot += player.bet(self.smallBlind)
                continue

            # show if is big blind
            if i == 1:
                print(Fore.BLUE + player.name + ", eres la ciega grande: Q" + str(self.bigBlind) + Style.RESET_ALL)              
                
                # print an empty line
                print()

                # big blind msg
                input(Fore.GREEN + "Presiona enter para colocar la ciega grande..." + Style.RESET_ALL)
                self.pot += player.bet(self.bigBlind)
                continue

            # bets round
            self.blindTurn(player)

        # clear console
            os.system('cls' if os.name == 'nt' else 'clear')

        # welcome message
        self.welcome()

        # deal flop cards
        flop = self.deck.deal_flop()

        # show floop cards
        print("Flop: ")
        self.deck.showCards(flop)
        self.community_cards += flop

        # print an empty line
        print()

        for i, player in enumerate(self.players):
            # clear console
            os.system('cls' if os.name == 'nt' else 'clear')

            # welcome message
            self.welcome()

            # pot balance
            print("Bote: " + "Q" + str(self.pot))

            # print an empty line
            print()

            # show floop cards
            print("Flop: ")
            self.deck.showCards(flop)

            # print an empty line
            print()

            # turn of next player
            input(Fore.GREEN + "Turno de " + player.name + ", presiona enter..." + Style.RESET_ALL)

            # print an empty line
            print()

            print(Fore.YELLOW + "Cartas / " + player.name + Style.RESET_ALL + " - " + "Q" + str(player.balance))
            player.showCards()

            # print an empty line
            print()

            # bets round
            self.betsTurn(player)

        # deal turn card
        turn = self.deck.deal_turn()

        # show turn card
        print("Turn: ")
        self.deck.showCards([turn])
        self.community_cards += [turn]

        # print an empty line
        print()

        for i, player in enumerate(self.players):
            # clear console
            os.system('cls' if os.name == 'nt' else 'clear')

            # welcome message
            self.welcome()

            # pot balance
            print("Bote: " + "Q" + str(self.pot))

            # print an empty line
            print()

            # show floop cards
            print("Flop: ")
            self.deck.showCards(flop)

            # print an empty line
            print()

            # show turn card
            print("Turn: ")
            self.deck.showCards([turn])

            # print an empty line
            print()

            # turn of next player
            input(Fore.GREEN + "Turno de " + player.name + ", presiona enter..." + Style.RESET_ALL)

            # print an empty line
            print()

            print(Fore.YELLOW + "Cartas / " + player.name + Style.RESET_ALL + " - " + "Q" + str(player.balance))
            player.showCards()

            # print an empty line
            print()

            # bets round
            self.betsTurn(player)

        # deal river card
        river = self.deck.deal_river()
        
        # show river card
        print("River: ")
        self.deck.showCards([river])
        self.community_cards += [river]

        # print an empty line
        print()

        for i, player in enumerate(self.players):
            # clear console
            os.system('cls' if os.name == 'nt' else 'clear')

            # welcome message
            self.welcome()

            # pot balance
            print("Bote: " + "Q" + str(self.pot))

            # print an empty line
            print()

            # show floop cards
            print("Flop: ")
            self.deck.showCards(flop)

            # print an empty line
            print()

            # show turn card
            print("Turn: ")
            self.deck.showCards([turn])

            # print an empty line
            print()

            # show river card
            print("River: ")
            self.deck.showCards([river])

            # print an empty line
            print()

            # turn of next player
            input(Fore.GREEN + "Turno de " + player.name + ", presiona enter..." + Style.RESET_ALL)

            # print an empty line
            print()

            print(Fore.YELLOW + "Cartas / " + player.name + Style.RESET_ALL + " - " + "Q" + str(player.balance))
            player.showCards()

            # print an empty line
            print()

            # bets round
            self.betsTurn(player)

        # clear console
        os.system('cls' if os.name == 'nt' else 'clear')

        # welcome message
        self.welcome()

        # pot balance
        print("Bote: " + "Q" + str(self.pot))

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

        # quit cards of all players
        for player in self.players:
            player.clearCards()

# clear console
os.system('cls' if os.name == 'nt' else 'clear')

game = Game()

# start the game 
game.welcome() 
game.init()
game.start()

# game loop
while(1):
    game.start()
