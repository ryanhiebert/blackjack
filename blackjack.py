#!/usr/bin/python
from __future__ import print_function, unicode_literals
import random

SUITS = SPADES, CLUBS, HEARTS, DIAMONDS = '\u2660\u2663\u2665\u2666'
RANKS = tuple('A23456789') + ('10', 'J', 'Q', 'K')

COLORS = 'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE'

try:
    input = raw_input
    str = unicode
except NameError:
    pass

def colorize(text, color_name='RED', bold=False):
    return '\033[{0};{1}m{2}\033[0m'.format(
        int(bold), COLORS.index(color_name), text)

def score(hand):
    score, aces = 0, 0
    for card in hand:
        rank = card[1:]
        if rank in tuple('JQK'):
            score += 10
        elif rank == 'A':
            aces += 1
        else:
            score += RANKS.index(rank) + 1
    scorelist = [score + aces]
    for ace in range(aces):
        scorelist.append(scorelist[-1] + 10)
    return tuple(scorelist)

def colored_card(card):
    card = card[0] + ' ' + card[1:]
    if card[0] in SUITS[-2:]:
        card = colorize(card)
    return card

def deep(hand):
    """Checks if a player's hand is deep (has been split)"""
    return len(hand) > 1 and len(hand[0]) > 1 and len(hand[0][0]) > 1

def out_game(player, dealer):
    """Write the state of the game to the screen"""
    dealer_out = 'Dealer: ' + str(score(dealer)) + ' - '
    for i, card in enumerate(dealer):
        dealer_out += colored_card(card)
        if i + 1 < len(dealer):
            dealer_out += ','
    len_dealer_out = len(dealer_out)
    dealer_out += (' ' * (30 - len_dealer_out)) + '  |  '
    
    if deep(player):
        player_out = 'Player: ' + 'a: ' + str(score(player)) + ' - '
        for i, hand in enumerate(player):
            if i > 0:
                player_out += ' ' * (len(dealer_out) + 8)
            player_out += 'abcd'[i] + ': ' + str(score(hand)) + ' - '
            for j, card in enumerate(hand):
                player_out += colored_card(card)
                if j + 1 < len(hand):
                    player_out += ','
            if i + 1 < len(player):
                player_out += '\n'
    else:
        player_out = 'Player: ' + str(score(player)) + ' - '
        for i, card in enumerate(player):
            player_out += colored_card(card)
            if i + 1 < len(player):
                player_out += ','
    print(dealer_out + player_out)

while True:
    try:
        decks = int(input('How Many Decks? '))
        if decks < 1:
            print('Please Enter a Natural Number higher than 0.')
        else:
            break
    except ValueError:
        print('Please Enter an Integer.')
    except (KeyboardInterrupt, EOFError):
        print()
        raise SystemExit

pot = 100
while True:
    deck = [suit + rank for suit in SUITS for rank in RANKS] * decks
    print('Shuffling the deck')
    random.shuffle(deck)
    while True:
        player, dealer = [], []
        print('Pot: ' + str(pot))
        while True:
            try:
                bet = int(input('Place Your Bet: '))
                if bet > pot:
                    print('You don\'t have enough in your pot.')
                elif bet < 0:
                    print('Please Enter a Natural Number higher than 0.')
                else:
                    pot -= bet
                    print('Pot: ' + str(pot))
                    break
            except ValueError:
                print('Please Enter an Integer')
            except (KeyboardInterrupt, EOFError):
                print()
                raise SystemExit
        dealer.append(deck.pop())
        player.append(deck.pop())
        player.append(deck.pop())
        out_game(player, dealer)
        while True:
            if score(player)[0] > 21 or 21 in score(player):
                break
            try:
                choice = input('(h)it, (s)tand, or (d)ouble down? ')
            except (KeyboardInterrupt, EOFError):
                print()
                raise SystemExit
            if choice == 'h' or choice == 'H':
                player.append(deck.pop())
                out_game(player, dealer)
            elif choice == 's' or choice == 'S':
                break
            elif (choice == 'd' or choice == 'D'):
                if pot > bet:
                    pot -= bet
                    bet *- 2
                    player.append(deck.pop())
                    out_game(player, dealer)
                    break
                else:
                    print('You don\'t have enough in your pot.')
            else:
                print('Invalid Selection.')
        if score(player)[0] > 21:
            print('Bust!')
            bet = 0
        else:
            if 21 in score(player):
                print('BlackJack!')
            dealer.append(deck.pop())
            if score(dealer)[0] > 21:
                print('Dealer Bust!')
            elif 21 in score(dealer):
                print('Dealer BlackJack!')
            else:
                for x in score(dealer):
                    if x <= 21:
                        dealer_score = x
                while dealer_score < 17:
                    dealer.append(deck.pop())
                    for x in score(dealer):
                        if x <= 21:
                            dealer_score = x
                if 21 in score(dealer):
                    print('Dealer BlackJack!')
                elif score(dealer)[0] > 21:
                    print('Dealer Bust!')
            out_game(player, dealer)
            for x in score(player):
                if x <= 21:
                    player_score = x
            for x in score(dealer):
                if x <= 21:
                    dealer_score = x
            if player_score == dealer_score:
                print('Tie Game, bet returned to pot.')
                pot += bet
                bet = 0
            elif player_score < dealer_score:
                print('You Lose, better luck next time. Bet forfeit.')
                bet = 0
            else:
                msg = 'You Win! You bet {0}, so your pot is now {1} richer!'
                print(msg.format(str(bet), str(bet * 2)))

        if ((decks == 1 and len(deck) < 17) or
            (decks == 2 and len(deck) < 24) or
            (decks == 3 and len(deck) < 25)):
            break
        elif decks in range(4, 11) and len(deck) < (29 + (decks - 4) * 2):
            break
        elif decks > 11 and len(deck) < 42:
            break
        else:
            try:
                cont = input('Would you like to shuffle the deck? (y/N)')
            except (KeyboardInterrupt, EOFError):
                print()
                raise SystemExit
            if cont in tuple('yY'):
                break
    if pot < 1:
        print('You are all out of money.  Goodbye :-(')
        break
