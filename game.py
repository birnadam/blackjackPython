from deck import Deck
from player import Player
from bot import Bot
from deck import Deck
import time as t
from not_enough_chips_exception import NotEnoughChipsError


class Game:
    def __init__(self, deck: Deck, player: Player, bot: Bot):
        self.deck = deck
        self.placed_bet = None
        self.player = player
        self.bot = bot
        self.player_busted = False
        self.bot_busted = False

    @classmethod
    def create_game(cls):
        deck = Deck()
        deck.shuffle()
        player = Player("You")
        bot = Bot("The Dealer")

        return cls(deck, player, bot)

    def show_hands_hidden(self):
        print("Your hand: {} {}   Dealer's hand: {} {} or higher".format(self.player.show_hand(
        ), self.player.calc_hand(), self.bot.show_hand_hidden(), self.bot.calc_hand_hidden()))

    def show_hands(self):
        print("Your hand: {} {}   Dealer's hand: {} {}".format(self.player.show_hand(
        ), self.player.calc_hand(), self.bot.show_hand(), self.bot.calc_hand()))

    def prepare_round(self):
        if len(self.deck.cards) <= 20:

            self.bot_busted = False
            self.player_busted = False

            print("The deck only has 20 cards left and was shuffled")
            self.deck.shuffle()
            print()

        self.discard_hands()
        self.draw_hands(0.5)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def discard_hands(self):
        self.player.discard_hand()
        self.bot.discard_hand()

    def draw_hands(self, delay: float = 0):
        for i in range(2):
            self.player.draw_card(self.deck)
            t.sleep(delay)
            self.bot.draw_card(self.deck)
            t.sleep(delay)
            print()

    def take_bet(self, player: Player):
        print("Your chips: {}$".format(player.chips))
        bet = input("Please place your bet: ")
        print()

        if type(bet) is not int:
            bet = int(bet)

        while True:
            try:
                player.place_bet(bet)
                self.placed_bet = bet
                break
            except NotEnoughChipsError as e:
                print("You don't have enough chips")
                continue

    def clear_bet(self):
        self.placed_bet = None
