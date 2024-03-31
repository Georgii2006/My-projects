#This program is my own realization of a card game called Durak
#you can read rules of the game via https://en.wikipedia.org/wiki/Durak

from random import *

ranks = ['2', '3', '4', '5',
         '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['♣', '♦', '♥', '♠']

def check(bot_card, user_card, trump):
    ranks = ['2', '3', '4', '5',
         '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    suits = ['♣', '♦', '♥', '♠']
    if bot_card[-1] == user_card[-1]:
        if ranks.index(bot_card[:-1]) < ranks.index(user_card[:-1]):
            return True
        else:
            return False
    else:
        if user_card[-1] == trump:
            return True
        else:
            return False

def responce_values(used_cards, bot_cards, trump, ranks):
    bot_values = []
    used_values = []
    for card in bot_cards:
        value = ranks.index(card[:-1])
        if card[-1] == trump:
            value += 100
        i = bot_cards.index(card)
        bot_values.append((value, i, card[-1], card))
    for i in range(len(used_cards)):
        pair = used_cards[i]
        if len(pair) == 0:
            continue
        card = pair[0]
        value = ranks.index(card[:-1])
        if card[-1] == trump:
            value += 100
        used_values.append((value, i, card[-1], card))
    return sorted(used_values), sorted(bot_values)
        
def bot_responce(used_cards, bot_cards, trump, deck, ranks):
    bot_gave_up = False
    responce_journal = []
    used_values, bot_values = responce_values(used_cards, bot_cards, trump, ranks)
    for used_value in used_values:
        current_pair = used_cards[used_value[1]]
        if len(current_pair) == 2:
            continue
        for bot_value in bot_values:
            if bot_value:
                if used_value[2] == bot_value[2]:
                    if bot_value[0] > used_value[0]:
                        x = bot_value[1]
                        y = used_value[1]
                        card = bot_cards[x]
                        used_cards[y].append(card)
                        del bot_cards[x]
                        z = bot_values.index(bot_value)
                        del bot_values[x]
                        responce_journal.append([used_value[3], bot_value[3]])
                        break
                if bot_value[2] == trump:
                    if bot_value[0] > used_value[0]:
                        x = bot_value[1]
                        y = used_value[1]
                        card = bot_cards[x]
                        used_cards[y].append(card)
                        del bot_cards[x]
                        z = bot_values.index(bot_value)
                        bot_values[x] = None
                        responce_journal.append([used_value[3], bot_value[3]])
                        break
    for pair in used_cards:
        if len(pair) < 2:
            print('-----------------------------------------')
            print('bot gave up and took all the cards'.upper())
            print('you can continue your attack or finish it')
            print('-----------------------------------------')
            bot_gave_up = True
            break
    else:
        for pair in responce_journal:
            length = len('BOT BEATS %s WITH %s' % (pair[0], pair[1]))
            print('-'*length)
            print('BOT BEATS %s WITH %s' % (pair[0], pair[1]))
            print('-'*length)
        
    return bot_gave_up, used_cards, bot_cards
def add_cards(cards, deck):
    while len(cards) < 6:
        if len(deck) < 1:
            break
        chosen_card = choice(deck)
        del deck[deck.index(chosen_card)]
        cards.append(chosen_card)
    return cards, deck
def cards_displaying(user_cards, deck, trump):
    print('\n\n')
    if len(user_cards) < 1:
        print("you don't have any cards")
        print('\n')
    print('trump: ', trump)
    print('cards in deck :', len(deck))
    print('your cards:')
    x = 1
    for card in user_cards:
        print(str(x) + ': ' + card)
        x += 1
def card_values(bot_cards, used_cards, ranks, trump):
    values = []
    bot_ranks = []
    used_ranks = []
    for pair in used_cards:
        for card in pair:
            used_ranks.append(card[:-1])
    for card in bot_cards:
        bot_ranks.append(card[:-1])
    for card in bot_cards:
        value = ranks.index(card[:-1])
        if card[-1] == trump:
            value += 100
        values.append(value)
    return values, bot_ranks, used_ranks
def bot_choice(bot_cards, used_cards, deck, trump):
    report_journal = []
    used_length = len(used_cards)
    values, bot_ranks, used_ranks = card_values(bot_cards, used_cards, ranks, trump)
    if len(used_cards) == 0:
            i = values.index(min(values))
            new_pair = []
            used_cards.append([bot_cards[i]])
            report_journal.append(bot_cards[i])
            del bot_ranks[i]
            del bot_cards[i]
    index_correction = 0
    breakable = False
    for i in range(len(bot_ranks)):
        for rank2 in used_ranks:
            if bot_ranks[i-index_correction] == rank2:
                if values[i+index_correction] < 100:
                    new_pair = []
                    used_cards.append([bot_cards[i]])
                    report_journal.append(bot_cards[i-index_correction])
                    del bot_ranks[i-index_correction]
                    del bot_cards[i-index_correction]
                    index_correction += 1
                    if len(used_cards) - 1 == used_length:
                        breakable = True
                        break
        if breakable:
            break
    breakable = False
    
    if used_length == len(used_cards):
        bot_stopped = True
    else:
        bot_stopped = False
    for card in report_journal:
        print('bot chose ' + card)
    return bot_cards, used_cards, bot_stopped
    
def user_turn(user_cards, bot_cards, deck, trump, ranks):
    print('--------------------------')
    print("------user's attack-------")
    print('--------------------------')
    bot_gave_up = False
    used_cards = []
    while True:
        cards_displaying(user_cards, deck, trump)
        print('type the index number of the card and press enter')
        if len(used_cards) > 0:
            print("type 0 and press enter if you want to finish attack")
        x = input()
        if not x.isdigit():
            print('the input is not valid')
            continue
        if len(used_cards) > 0:
            if x == '0':
                break
        if  int(x) < 1 or int(x) > len(user_cards):
            print('you have chosen incorrect index number')
            continue
        chosen_card = user_cards[int(x)-1]
        breakable = False
        if len(used_cards) > 0:
            for pair in used_cards:
                for card in pair:
                    if card[:-1] == chosen_card[:-1]:
                        breakable = True
                        break
                if breakable:
                    break
            else:
                print('the card you chose must have the same rank with at at least one card\n that was used during this turn')
                continue
        breakable = False
        pair = [user_cards[int(x)-1]]
        used_cards.append(pair)
        del user_cards[int(x)-1]
        if not bot_gave_up:
            bot_gave_up, used_cards, bot_cards = bot_responce(used_cards, bot_cards, trump, deck, ranks)
        if bot_gave_up:
            for pair in used_cards:
                for card in pair:
                    if not card in bot_cards:
                        print('bot took ' + card)
                        bot_cards.append(card)
    return user_cards, bot_cards, deck, bot_gave_up
def bot_turn(user_cards, bot_cards, deck, trump, ranks):
    print('-------------------------')
    print("------bot's attack-------")
    print('-------------------------')
    user_gave_up = False
    bot_stopped = False
    used_cards = []
    while not bot_stopped:
        bot_cards, used_cards, bot_stopped = bot_choice(bot_cards, used_cards, deck, trump)
        displaying = False
        for pair in used_cards:
            if len(pair) < 2:
                displaying = True
                break
        if not user_gave_up and displaying:
            cards_displaying(user_cards, deck, trump)
        while not user_gave_up:
            for pair in used_cards:
                if len(pair) < 2:
                    break
            else:
                break
            number = 1
            proposed_cards = []
            while not user_gave_up:
                print('type index number of the card and press enter')
                print('type 0 and press enter if you want to pick up all cards')
                y = input()
                if not y.isdigit():
                    print('you should write a number')
                    continue
                if y == '0':
                    print('you took all the cards')
                    user_gave_up = True
                    break
                if int(y) < 0:
                    print('you chose incorrect number')
                    continue
                if check(used_cards[-1][0], user_cards[int(y)-1], trump):
                    used_cards[-1].append(user_cards[int(y)-1])
                    print('\n\n')
                    length = len('YOU BEAT %s WITH %s' % (used_cards[-1][0], user_cards[int(y)-1]))
                    print('-'*length)      
                    print('YOU BEAT %s WITH %s' % (used_cards[-1][0], user_cards[int(y)-1]))
                    print('-'*length)
                    del user_cards[int(y)-1]
                    break
                else:
                    print('you chose incorrect card')
            if user_gave_up:
                for pair in used_cards:
                    for card in pair:
                        if not card in user_cards:
                            print('you took ' + card)
                            user_cards.append(card)
    print('------------------')
    print('bot finished atack')
    print('------------------')
    return user_cards, bot_cards, deck, user_gave_up
def create_deck(ranks, suits):
    deck = []
    for rank in ranks:
        for suit in suits:
            deck.append(rank+suit)
    return deck


    
def game(ranks, suits):
    deck = create_deck(ranks, suits)
    previous_turn = 0
    trump = choice(suits)
    user_cards = []
    bot_cards = []
    used_cards = []
    bot_gave_up = False
    user_gave_up = False
    turn = choice([0,1])
    while True:
        print('playing with 52 has not been tested yet')
        print('choose deck')
        print('type 1 and press enter for 36 cards')
        print('type 2 and press enter for 52 cards')
        print('type 3 and press enter to exit')
        a = input()
        if a == '1':
            deck = create_deck(ranks[4:], suits)
            break
        if a == '2':
            deck = create_deck(ranks, suits)
            break
        if a == '3':
            print('game over')
            return
    while True:
        print('\n\n')
        if turn == 1 and not bot_gave_up:
            turn = 0
        elif turn == 0 and not user_gave_up:
            turn = 1
        if previous_turn:
            user_cards, deck = add_cards(user_cards, deck)
            bot_cards, deck = add_cards(bot_cards, deck)
        else:
            bot_cards, deck = add_cards(bot_cards, deck)
            user_cards, deck = add_cards(user_cards, deck)
        if len(user_cards) == 0 and len(deck) == 0:
            print('--------')
            print('user win')
            print('--------')
            return
        if len(bot_cards) == 0 and len(deck) == 0:
            print('-------')
            print('bot won')
            print('-------')
            return
        if turn:
            user_cards, bot_cards, deck, bot_gave_up = user_turn(user_cards, bot_cards, deck,
                                                                 trump, ranks)
        else:
            user_cards, bot_cards, deck, user_gave_up = bot_turn(user_cards, bot_cards,
                                                                 deck, trump, ranks)
        previous_turn = turn

game(ranks, suits)
