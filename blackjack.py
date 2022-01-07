from random import shuffle
from abc import ABC, abstractmethod


class Deck:

    def __init__(self):
        '''
        The purpose of this class is to create the deck of 52 cards and it can shuffle and
        pop cards from top of the deck to players or dealer. There are three attribute, which
        are ranks, suits and cards. The ranks is the rank in the deck, which is number from 2
        to 10 and "J", "Q", "K" and "A". The suits is the suit in the deck, which is include
        'spades', 'diamonds', 'clubs' and 'hearts'. The cards is the each card in the deck,
        which contain the rank and suit for each card. Each card have rank and suit attributes,
        save in a tuple.
        '''
        ranks = [str(n) for n in range(2, 11)] + ['J', 'Q', 'K', 'A']
        suits = ['spades', 'diamonds', 'clubs', 'hearts']
        self.cards = [(rank, suit) for suit in suits for rank in ranks]

    def deal_card(self):
        '''
        The purpose of this function is to pop top of the card from the deck, give it to the player
        or dealer.
        Returns:
            return is the card attribute.
        '''

        return self.cards.pop(0)

    def shuffle(self):
        '''
        The purpose of this function is to shuffle the deck to make it random.
        Returns:
            Nothing for return for this function
        '''
        shuffle(self.cards)


class Game:
    def __init__(self, human_player=1, computer_player=1):
        '''
        The purpose of the this class is create the game. There are three attributes, which are
        deck, players and dealer. The players is a list of player,which is include all human
        players and computer players instances. The dealer attribute is a dealer in the game,
        which is an instance of Dealer() class. And the deck attribute is a deck we use in the
        game, which is an instance of Deck() class.

        Args:
            human_player: is a int type. It represents the human players in the game.
            computer_player: is a int type. It represents the computer players in the game.
        '''
        self.human_player = human_player
        self.computer_player = computer_player
        self.deck = Deck()
        self.players = []
        self.dealer = Dealer()

    def play(self):
        '''
        The purpose of this function is to start the blackjack game. We need to initialize
        all the instances in the beginning . First, we need to assign one card for each player
        and dealer. Then give other card for each player and dealer. And display all cards that
        each player have, and display the first card for dealer and hide the other one to display.
        Then each player have their own turn to decide hit or stand. Human players decide hit or
        stand by using user input, computer player decide hit or stand by checking that is point
        less than 19. And dealer decide hit or stand by checking that is point less than 17.
        When we finish all players and dealer turns, it going to decide who is the winner for
        this game. Then ask the user whether want to a new game.

        Returns:
            nothing for return.
        '''

        while True:
            self.deck = Deck()
            self.deck.shuffle()
            self.players = []
            self.dealer = Dealer()
            for num_human in range(self.human_player):
                human = HumanPlayer()
                human.setup_name(num_human)
                self.players.append(human)
            for num_computer in range(self.computer_player):
                computer = ComputerPlayer()
                computer.setup_name(num_computer)
                self.players.append(computer)
            print("Welcome to the Blackjack game.")
            print("Game start!!~")

            for each_player in self.players:  # Give each player first card
                each_player.contain_cards.append(self.deck.deal_card())
            self.dealer.contain_cards.append(self.deck.deal_card())

            for each_player in self.players:  # Give each player second card
                each_player.contain_cards.append(self.deck.deal_card())
            self.dealer.contain_cards.append(self.deck.deal_card())

            for each_player in self.players:  # display all players and dealers cards
                each_player.display_info()
            self.dealer.hide_info()

            for each_player in self.players:  # for each player to decide hit or stand
                print("Now is " + each_player.name + " turn:")
                each_player.hit_or_stand(self.deck)
            print("Now is Dealer turn: ")
            self.dealer.display_info()  # display dealer cards
            self.dealer.hit_or_stand(self.deck)

            remove_list = []
            for ind, player in enumerate(self.players):  # to get the index for the points larger than 21
                if player.get_point()>21:
                    remove_list.append(ind)
            remove_list.reverse()       # remove in a reverse order.
            for ind in remove_list:     # remove players that pointer larger than 21
                self.players.pop(ind)
            candidate = []      # to contain all the player that with highest point.
            if self.players:    # if the list is not empty
                score_for_player = []   # to store the point less or equal to 21.
                for each_player in self.players:
                    score_for_player.append(each_player.get_point())
                highest = max(score_for_player)     # to get the highest point within 21

                winner_index = [index for index, value in  # to get the index that player get the same highest point
                                enumerate(score_for_player)
                                if value == highest]
                for index in winner_index:  # add the same highest point player into the candidate list
                    candidate.append(self.players[index])
            else:
                highest = 0

            if self.dealer.get_point()<=21:     # if dealer's point less than or equal to 21
                if self.dealer.get_point() > highest:
                    print("Dealer is the winner.")
                    print("The highest score is: " + str(self.dealer.get_point()))
                elif self.dealer.get_point() == highest:
                    all_name = ""
                    for cand in candidate:      # to get all of name have same point
                        all_name = all_name + cand.name + " "
                    print(all_name + "and Dealer have same points.")
                    print("Thus, this game is tie.")
                    print("The highest score is: " + str(self.dealer.get_point()))
                else:
                    all_name = ""
                    for cand in candidate:
                        all_name = all_name + cand.name + " "
                    print(all_name + "are winners.")
                    print("The highest score is: " + str(highest))
            else:       # if dealer busted
                if self.players:
                    all_name = ""
                    for cand in candidate:
                        all_name = all_name + cand.name + " "
                    print(all_name + "are winners.")
                    print("The highest score is: " + str(highest))
                else:
                    print("Everyone busted!~")
                    print("No winner for this game.")

            play_again = input("Do you want another round? (yes/no):")
            while play_again != "yes" and play_again != "no":
                play_again = input("Wrong input!~ Please input \"yes\" or \"no\"")
            if play_again == "no":
                print("Bye!~ See you next time!~ ")
                break


class Player(ABC):

    def __init__(self):
        '''
        The purpose of this class is the base class that inherent from ABC class.
        And this class will be inherited by HumanPlayer class and ComputerPlayer class.
        And this class have two attributes which are contain_cards and name. contain_cards
        is a list that store all cards for each player. And name is to specific the name
        for each human player and computer player.
        '''
        self.contain_cards = []
        self.name = ""

    @abstractmethod
    def setup_name(self, number):
        '''
        The purpose of this function is to set up a name for each human player and computer player.
        Args:
            number: is a int type. It is just a number order of human players or computer players.
                    For example, we have two human player, the name are human player 1 and
                    human player 2.
        Returns:
            nothing return for this function.
        '''
        raise NotImplemented

    @abstractmethod
    def display_info(self):
        '''
        The purpose of this function is to display player's name and all cards in the player's hand.
        Returns:
            nothing return for this function.
        '''
        raise NotImplemented

    @abstractmethod
    def get_point(self):
        '''
        The purpose of this function is to calculate the point for player. First, decide the value for
        2-10 , "J", "Q" and "K". When finish to compute each value other than "A". Then we decide the
        "A" value based on whether the total points is greater than 11 or not. If so, "A" is the value
        of 1. Otherwise, "A" is the value of 11.
        Returns:
            The return is the int type. And it returns the total points in the players hand.
        '''
        raise NotImplemented

    @abstractmethod
    def hit_or_stand(self, deck):
        '''
        The purpose of this function is to decide player want to hit or stand. The human player is
        simple to decide by the user input. When input is "hit" human player will get a new card.
        And when input is "stand" human player don't want a new card. For computer player, I used
        the naive way to decide the computer player want to hit or stand. When the total point of
        computer player is less than 19, they will need a new card. Otherwise, they will "stand" it.
        Args:
            deck: deck is the instance of Deck() which created in the play() function. It can help
            player to get a new card from the top of the deck, when they decide "hit" to increase
            their total points.

        Returns:
            nothing return for this function.
        '''
        raise NotImplemented


class HumanPlayer(Player):

    def setup_name(self, number):
        '''
        The purpose of this function is to set up a name for each human player.
        Args:
            number: it is a int type. It is just a number order of human players.
            For example, we have two human player, the name are human player 1 and
            human player 2.

        Returns:
            nothing return for this function.
        '''

        self.name = "Human player " + str((number + 1))

    def display_info(self):
        '''
        The purpose of this function is to display  human player's name and all cards
        Returns:
            nothing return for this function.
        '''
        print("\t" + self.name + " has" + str(self.contain_cards))

    def get_point(self):
        '''
        The purpose of this function is to calculate the point for human player. First, decide the value
        for 2-10 , "J", "Q" and "K". When finish to compute each value other than "A". Then we decide the
        "A" value based on whether the total points is greater than 11 or not. If so, "A" is the value
        of 1. Otherwise, "A" is the value of 11.
        Returns:
            The return is the int type. And it returns the total points in the human players hand.
        '''

        points = 0
        for index in range(len(self.contain_cards)):
            if "J" in self.contain_cards[index][0]:
                points += 10
            elif "Q" in self.contain_cards[index][0]:
                points += 10
            elif "K" in self.contain_cards[index][0]:
                points += 10
            elif self.contain_cards[index][0].isdigit():
                points += int(self.contain_cards[index][0])

        for index in range(len(self.contain_cards)):
            if "A" in self.contain_cards[index][0]:
                if points < 11:
                    points += 11
                else:
                    points += 1

        return points

    def hit_or_stand(self, deck):
        '''
        The purpose of this function is to decide human player want to hit or stand. The human
        player is simple to decide by the user input. When input is "hit" human player will
        get a new card. And when input is "stand" human player don't want a new card.
        Args:
            deck: deck is the instance of Deck() which created in the play() function. It can help
            human player to get a new card from the top of the deck, when they decide "hit" to increase
            their total points.

        Returns:
            nothing return for this function.
        '''
        while True:
            human_input = input("\tDo you want to hit or stand: ")
            if human_input == "hit":
                self.contain_cards.append(deck.deal_card())
                self.display_info()
                print("\t" + self.name + " point is:" + str(self.get_point()))
                if self.get_point() > 21:
                    print("\t" + self.name + " is busted since point is: " + str(self.get_point()))
                    break
            elif human_input == "stand":
                self.display_info()
                print("\t" + self.name + " point is: " + str(self.get_point()))
                break
            else:
                print("Wrong input!~ Please type in \"hit\" or \"stand\"")


class ComputerPlayer(Player):

    def setup_name(self, number):
        '''
        The purpose of this function is to set up a name for each computer player.
        Args:
            number: it is a int type. It is just a number order of computer players. For example,
            we have two computer players, the name are computer player 1 and computer player 2.

        Returns:
            nothing return for this function.
        '''
        self.name = "Computer player " + str((number + 1))

    def display_info(self):
        '''
        The purpose of this function is to display computer player's name and all cards
        in the computer player's hand.
        Returns:
            nothing return for this function.
        '''

        print("\t" + self.name + " has" + str(self.contain_cards))

    def get_point(self):
        '''
        The purpose of this function is to calculate the point for computer player. First, decide the value
        for 2-10 , "J", "Q" and "K". When finish to compute each value other than "A". Then we decide the
        "A" value based on whether the total points is greater than 11 or not. If so, "A" is the value
        of 1. Otherwise, "A" is the value of 11.
        Returns:
            The return is the int type. And it returns the total points in the computer players hand.
        '''
        points = 0
        for index in range(len(self.contain_cards)):
            if "J" in self.contain_cards[index][0]:
                points += 10
            elif "Q" in self.contain_cards[index][0]:
                points += 10
            elif "K" in self.contain_cards[index][0]:
                points += 10
            elif self.contain_cards[index][0].isdigit():
                points += int(self.contain_cards[index][0])

        for index in range(len(self.contain_cards)):
            if "A" in self.contain_cards[index][0]:
                if points < 11:
                    points += 11
                else:
                    points += 1

        return points

    def hit_or_stand(self, deck):
        '''
        The purpose of this function is to decide computer player want to hit or stand.
        For computer player, I used the naive way to decide the computer player want to
        hit or stand. When the total point of computer player is less than 19, they will
        need a new card. Otherwise, they will "stand" it.
        Args:
            deck: deck is the instance of Deck() which created in the play() function.
            It can help computer player to get a new card from the top of the deck,
            when they decide "hit" to increase their total points.

        Returns:
            nothing for return.
        '''
        if self.get_point() >= 19:
            print("\t" + self.name + " choose stand")
            self.display_info()
        print("\t" + self.name + " point is: " + str(self.get_point()))
        while self.get_point() < 19:

            print("\t" + self.name + " choose hit")
            self.contain_cards.append(deck.deal_card())
            self.display_info()
            if self.get_point() > 21:
                print("\t" + self.name + " is busted since point is: " + str(self.get_point()))
                break
            elif 19 <= self.get_point() <= 21:
                print("\t" + self.name + " choose stand")
                print("\t" + self.name + " point is: " + str(self.get_point()))
            else:
                print("\t" + self.name + " point is: " + str(self.get_point()))


class Dealer:

    def __init__(self):
        '''
        The purpose of this class is to create a Dealer class, which is include the attribute
        "contain_cards", can store all cards in the dealer hand.
        '''
        self.contain_cards = []

    def hide_info(self):
        '''
        The purpose of this function is to output the first of dealer's card and hide the other
        one, which contain in the list.
        Returns:
            nothing return for this function.
        '''
        deal_cards = [self.contain_cards[0], "****"]
        print("\tDealer has" + str(deal_cards))

    def display_info(self):
        '''
        The purpose of this function is to display all cards in the player's hand.
        Returns:
            nothing return for this function.
        '''
        print("\tDealer has" + str(self.contain_cards))

    def get_point(self):
        '''
        The purpose of this function is to calculate the point for player. First, decide the value for
        2-10 , "J", "Q" and "K". When finish to compute each value other than "A". Then we decide the
        "A" value based on whether the total points is greater than 11 or not. If so, "A" is the value
        of 1. Otherwise, "A" is the value of 11.
        Returns:
            The return is the int type. And it returns the total points in dealer's hand.
        '''
        points = 0
        for index in range(len(self.contain_cards)):
            if "J" in self.contain_cards[index][0]:
                points += 10
            elif "Q" in self.contain_cards[index][0]:
                points += 10
            elif "K" in self.contain_cards[index][0]:
                points += 10
            elif self.contain_cards[index][0].isdigit():
                points += int(self.contain_cards[index][0])

        for index in range(len(self.contain_cards)):  # since we need to decide A value in last minutes
            if "A" in self.contain_cards[index][0]:
                if points < 11:
                    points += 11
                else:
                    points += 1
        return points

    def hit_or_stand(self, deck):
        '''
        The purpose of this function is to decide the dealer want to "hit" or "stand". When dealer's
        total point is less than 17, they will "hit" to get a new card from the top of the deck.
        Otherwise, they will choose "stand".
        Args:
            deck: deck is the instance of Deck() which created in the play() function.
            It can help dealer to get a new card from the top of the deck, when they
            decide "hit" to increase their total points.
        Returns:
            nothing return for this function.
        '''
        if self.get_point() >= 17:
            print("\tDealer choose stand since point larger than or equal to 17")
        print("\tNow dealer point is: " + str(self.get_point()))
        while self.get_point() < 17:
            print("\tDealer choose hit since dealer point less than 17 ")
            self.contain_cards.append(deck.deal_card())
            self.display_info()
            print("\tNow dealer point is: " + str(self.get_point()))
            if self.get_point() > 21:
                print("\tDealer busted since point is: " + str(self.get_point()))
                break
            elif 17 <= self.get_point() <= 21:
                print("\tDealer choose stand")


if __name__ == '__main__':
    game = Game()
    game.play()
