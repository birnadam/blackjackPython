import time as t
from game import Game

if __name__ == "__main__":
    game = Game.create_game()

    with game.player as p:
        with game.bot as bot:
            while p.chips > 0:
                if game.placed_bet != None:
                    game.clear_bet()
                # Players start without being busted
                game.prepare_round()
                game.bot_busted = False
                game.player_busted = False
                print("New hands; busted reset to False for both Players")

                # Prints starting hands 
                game.show_hands_hidden()
                game.take_bet(game.player)

                while True:
                    print("Your chips: {}$   Your bet: {}$".format(
                        p.chips, game.placed_bet))
                    # Once someone busts reveal dealer's hand
                    game.show_hands_hidden()
                    print()
                    inp = input("Would you like to hit? Y/N  ")
                    print()

                    inp = str.lower(inp)
                # Beneath this is conditional logic for whether or not the game continues and whether or not a new card is handed to player/dealer
                    if inp == "y":
                        if not p.draw_card(game.deck):
                            game.player_busted = True

                            print()
                            game.show_hands()
                            print("{} busted".format(p.name))
                            print("{} lost {}$".format(
                                p.name, game.placed_bet))
                            # Reveals both hands
                            print()
                            break
                    elif inp == "n":
                        print("Start of round: Player busted = {}, Bot busted = {}".format(
                            game.player_busted, game.bot_busted))
                        break
                    
                    if not game.player_busted: # Game continues if player is not busted
                        if not inp == "y":
                            if bot.calc_hand() < 16:
                                if not bot.draw_card(game.deck):
                                    game.bot_busted = True
                                    print()
                                    print("{} busted".format(bot.name))
                                    game.show_hands()  # Reveals both hands
                                    print("You win {}$".format(
                                        game.placed_bet))
                                    p.chips += (game.placed_bet * 2)

                                    print()
                                    break

                if not game.player_busted:
                    while bot.calc_hand() < 16:
                        if not bot.draw_card(game.deck):
                            game.bot_busted = True
                            print()
                            game.show_hands()  # Reveals both hands
                            print("{} busted".format(bot.name))
                            print("You win {}$".format(game.placed_bet))
                            print()
                            p.chips += (game.placed_bet * 2)

                            break
                        t.sleep(0.5)

                if game.bot_busted != True and game.player_busted != True:
                    print("No one busted")
                    if p.calc_hand() > bot.calc_hand() and p.calc_hand() < 22 and bot.calc_hand() < 22:
                        print("{} wins {}$".format(
                            p.name, (game.placed_bet * 2)))
                        game.show_hands()
                        print()
                        p.chips += (game.placed_bet * 2)
                    else:
                        print("{} wins".format(bot.name))
                        game.show_hands()
                        print("You lose {}$".format(game.placed_bet))
                        print()

                print("Result: Player busted = {}, Dealer busted = {}".format(
                    game.player_busted, game.bot_busted))
                print("New game begins in 5 seconds")
                print()
                t.sleep(5)