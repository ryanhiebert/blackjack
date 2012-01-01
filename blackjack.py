#!/usr/bin/python
from __future__ import print_function, unicode_literals
import random

try: input, str = raw_input, unicode
except NameError: pass

SUITS = SPADES, CLUBS, HEARTS, DIAMONDS = '\u2660\u2663\u2665\u2666'
RANKS = tuple('A23456789') + ('10', 'J', 'Q', 'K')
COLORS = 'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE'

def colorize(text, color, bold=False):
    template = '\033[{0};{1}m{2}\033[0m'
    return template.format(int(bold), COLORS.index(color) + 30, text)

class Player(object):
    """A player in a BlackJack game"""
    def __init__(self, pot=None):
        """set pot and set hands as []"""
        self.pot, self.hands = pot, []

class Card(str):
    def colored(self):
        """Return colored card for printing"""
        card = self[0] + ' ' + self[1:]
        if card[0] in (HEARTS, DIAMONDS):
            card = colorize(card, 'RED')
        return card

class Hand(list):
    def score(self):
        """Count the score of this hand"""
        score, aces = 0, 0
        for card in self:
            rank = card[1:]
            if rank in RANKS[-3]:
                score += 10
            elif rank != 'A':
                score += RANKS.index(rank) + 1
        scores = [score + aces]
        for ace in range(aces):
            scores.append(scorelist[-1] + 10)
        return tuple(scores)

    def out(self):
        """Return a string of the state of the hand, for printing"""
        out = ''
        for i, card in enumerate(self):
            out += card.colored()
            if i + 1 < len(self):
                out += ','
        return out

class Game(object):
    def __init__(self, decks):
        """Create a game with a given number of decks and a starting pot"""
        self.decks = decks
        self.pot = pot
        self.reset()

    def reset(self):
        normal_deck = [Card(suit + rank) for suit in SUITS for rank in RANKS]
        self.deck = normal_deck * self.decks
        random.shuffle(self.deck)

    def out(self):
        """Return a string of the state of the game, for printing"""
        dealer_out = 'Dealer: ' + str(self.dealer.hands[0].score()) + ' - '
        dealer_out += self.dealer.hands[0].out()
        if len(dealer_out) < 30:
            dealer_out += ('' * (30 - len(dealer_out))) + '  |  '
        player_out = 'Player: '
        if len(self.players[0].hands) > 1:
            for i, hand in enumerate(self.players[0].hands):
                if i > 0:
                    player_out += ' ' * (len(dealer_out) + 8)
                player_out += 'abc'[i] + ': ' + str(hand.score()) + ' - '
                player_out += hand.out() + '\n'
            player_out = player_out[:-1] # Remove Final Newline
        else:
            player_out += str(self.players[0].hands[0].score()) + ' - '
            player_out += self.players[0].hands[0].out()
        return dealer_out + player_out

def get_input(*args, **kwargs):
    """A wrapper for the input function to exit cleanly on ^D and ^C"""
    try:
        return input(*args, **kwargs)
    except (KeyboardInterrupt, EOFError):
        print()
        raise SystemExit

def get_bet(pot):
    print('Pot: ' + colorize(str(pot), 'GREEN') + '  ', end='')
    while True:
        try:
            bet = int(get_input('Place Your Bet: '))
            if bet > pot:
                print("You don't have enough in your pot.")
            elif bet < 1:
                print("You must bet more than 0.")
            else:
                break
        except ValueError:
            print('Please Enter an integer.')
    return bet

def get_int_input(name, default):
    while True:
        try:
            val = get_input('{0} ({1}): '.format(name, str(default)))
            if val == '':
                val = default
            else:
                val = int(val)
            if val < 1:
                print('{0} must be more than 0.'.format(name))
            else:
                break
        except ValueError:
            print('Please Enter an Integer.')
    return val

def best_score(hand):
    best_score = hand.score()[0]
    for score in hand.score()[1:]:
        if score <= 21:
            best_score = score
    return best_score

if __name__ == '__main__':
    decks = get_int_input('Number of Decks', 1)
    pot = get_int_input('Starting Pot', 100)

    game = Game(decks)
    players, dealer = game.players, game.dealer = [Player(pot)], Player()
    player, dealer = players[0], dealer
    
    while True:
        # Check if pot is empty
        if player.pot <= 0:
            print('Your pot is empty. You Lose. :-(')
            break

        # Start the game
        print('Shuffling the deck... ', end='')
        game.reset()
        print('done.')

        while True:
            # Deal
            player.hands = [Hand([game.deck.pop(), game.deck.pop()])]
            dealer.hands = [Hand([game.deck.pop()])]
            bet = get_bet(player.pot)
            player.hands[0].bet = bet
            player.pot -= bet
            print(game.out())
            while True:
                # Player's Turn
                hand = player.hands[0]
                if hand.score() > 21 or 21 in score:
                    break
                choice = get_input('(h)it, (s)tand, or (d)ouble down? ')
                if choice in tuple('hH'):
                    hand.append(game.deck.pop())
                    print(game.out())
                elif choice in tuple('sS'):
                    break
                elif choice in tuple('dD'):
                    if player.pot > 0:
                        bet = get_bet(player.pot)
                        hand.bet += bet
                        player.pot -= bet
                        hand.append(game.deck.pop())
                        print(game.out())
                        break
                    else:
                        print("You don't have anything in your pot.")
                else:
                    print('Invalid Selection.')

            if player.hands[0].score()[0] > 21:
                print('Bust!')
            else:
                if 21 in player.hands[0].score():
                    if len(player.hands[0]) == 2:
                        print('Blackjack!')
                    else:
                        print('21!')

                # Dealer's Turn
                hand = dealer.hands[0]
                hand.append(game.deck.pop())
                if hand.score()[0] > 21:
                    print(game.out())
                    print('Dealer Bust!')
                elif 21 in hand.score():
                    print(game.out())
                    print('Dealer BlackJack!')
                else:
                    while best_score(hand) <= 17:
                        hand.append(game.deck.pop())
                    print(game.out())
                    if 21 in hand.score():
                        print('Dealer 21!')
                    elif hand.score()[0] > 21:
                        print('Dealer Bust!')

            # Score the Game, Retrieve the Bets
            player_score = best_score(player.hands[0])
            dealer_score = best_score(dealer.hands[0])
            if player_score == dealer_score:
                print('Tie Game, bet returned to pot.')
                player.pot += player.hands[0].bet
            elif player_score < dealer_score:
                print('You Lose, better luck next time. Bet forfeit.')
            elif player_score == 21 and len(player.hands[0]) == 2:
                print('You get your bet plus 1.5x your bet!')
                player.pot += int(player.hands[0].bet * 2.5)
            else:
                print('You win th bet!')
                player.pot += player.hands[0].bet * 2
            
            # Decide whether to shuffle, or give the player the choice
            if ((game.decks == 1 and len(game.deck) < 17) or
                (game.decks == 2 and len(game.deck) < 24) or
                (game.decks == 3 and len(game.deck) < 25) or
                (game.decks in range(4,11) and
                 len(game.deck) < (29 + (game.decks - 4) * 2) or
                game.decks > 11 and len(game.deck) < 42)):
                break
            else:
                cont = get_input('Shuffle? (y/N) ')
                if cont in tuple('yY'):
                    break
