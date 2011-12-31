#!/usr/bin/python
from __future__ import print_function, unicode_literals
import random

SUITS = SPADES, CLUBS, HEARTS, DIAMONDS = '\u2660\u2663\u2665\u2666'
RANKS = tuple('A23456789') + ('10', 'J', 'Q', 'K')

try:
    input = raw_input
    str = unicode
except NameError:
    pass

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

def deep(hand):
    """Checks if a player's hand is deep (has been split)"""
    return len(hand) > 1 and len(hand[0]) > 1 and len(hand[0][0]) > 1

def out_game(player, dealer, pot):
    """Write the state of the game to the screen"""
    pot_out = 'Pot: ' + str(pot) + '\n'
    dealer_out = 'Dealer: ' + str(score(dealer)) + ' - '
    for i, card in enumerate(dealer):
        dealer_out += card[0] + ' ' + card[1:]
        if i + 1 < len(dealer):
            dealer_out += ','
    dealer_out += ' | '
    
    if deep(player):
        player_out = 'Player: ' + 'a: ' + str(score(player)) + ' - '
        for i, hand in enumerate(player):
            if i > 0:
                player_out += ' ' * (len(dealer_out) + 8)
            player_out += 'abcd'[i] + ': ' + str(score(hand)) + ' - '
            for j, card in enumerate(hand):
                player_out += card[0] + ' ' + card[1:]
                if j + 1 < len(hand):
                    player_out += ','
            if i + 1 < len(player):
                player_out += '\n'
    else:
        player_out = 'Player: ' + str(score(player)) + ' - '
        for i, card in enumerate(player):
            player_out += card[0] + ' ' + card[1:]
            if i + 1 < len(player):
                player_out += ','
    print('\n' + pot_out + dealer_out + player_out + '\n')

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
    random.shuffle(deck)
    while True:
        player, dealer = [], []
        out_game(player, dealer, pot)
        while True:
            try:
                bet = int(input('Place Your Bet: '))
                if bet > pot:
                    print('You don\'t have enough in your pot.')
                elif bet < 0:
                    print('Please Enter a Natural Number higher than 0.')
                else:
                    pot -= bet
                    break
            except ValueError:
                print('Please Enter an Integer')
            except (KeyboardInterrupt, EOFError):
                print()
                raise SystemExit
        dealer.append(deck.pop())
        player.append(deck.pop())
        player.append(deck.pop())
        out_game(player, dealer, pot)
        while True:
            if tuple(score(player))[0] > 21:
                break
            try:
                choice = input('(h)it, (s)tand, or (d)ouble down? ')
            except (KeyboardInterrupt, EOFError):
                print()
                raise SystemExit
            if choice == 'h' or choice == 'H':
                player.append(deck.pop())
                out_game(player, dealer, pot)
            elif choice == 's' or choice == 'S':
                break
            elif (choice == 'd' or choice == 'D'):
                if pot > bet:
                    player.append(deck.pop())
                    out_game(player, dealer, pot)
                    break
                else:
                    print('You don\'t have enough in your pot.')
            else:
                print('Invalid Selection.')
        if tuple(score(player))[0] > 21:
            print('Bust!')
            bet = 0
        else:
            if 21 in tuple(score(player)):
                print('BlackJack!')
            dealer.append(deck.pop())
            if tuple(score(dealer))[0] > 21:
                print('Dealer Bust!')
            elif 21 in tuple(score(dealer)):
                print('Dealer BlackJack!')
            else:
                for x in tuple(score(dealer)):
                    if x <= 21:
                        dealer_score = x
                while dealer_score < 17:
                    dealer.append(deck.pop())
                    for x in tuple(score(dealer)):
                        if x <= 21:
                            dealer_score = x
                if 21 in tuple(score(dealer)):
                    print('Dealer BlackJack!')
                elif tuple(score(dealer))[0] > 21:
                    print('Dealer Bust!')
            out_game(player, dealer, pot)
            for x in tuple(score(player)):
                if x <= 21:
                    player_score = x
            for x in tuple(score(dealer)):
                if x <= 21:
                    dealer_score = x
            if player_score == dealer_score:
                print('Tie Game, bet returned to pot.')
                pot += bet
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
            if cont in tuple('nN'):
                break
    if pot < 1:
        print('You are all out of money.  Goodbye :-(')
