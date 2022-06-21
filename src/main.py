from itertools import chain
from random import shuffle
import pandas as pd


def game_step(player1_deck, player2_deck):
    if player1_deck[0] > player2_deck[0]:  # first player win
        player1_deck, player2_deck = simple_win(player1_deck, player2_deck)
    elif player1_deck[0] < player2_deck[0]:  # Second player win
        player2_deck, player1_deck = simple_win(player2_deck, player1_deck)
    else:  # tie
        player1_deck, player2_deck = tie(player1_deck, player2_deck, recursion_num=0)
    return player1_deck, player2_deck


def simple_win(wining_deck, losing_deck):
    wining_card = wining_deck[0]
    losing_card = losing_deck[0]
    del losing_deck[0]
    del wining_deck[0]
    wining_deck.extend([wining_card, losing_card])
    return wining_deck, losing_deck


def tie_win(wining_deck, losing_deck, tie_loc):
    wining_cards = wining_deck[:tie_loc+1] if len(wining_deck) > tie_loc else wining_deck
    losing_cards = losing_deck[:tie_loc+1] if len(losing_deck) > tie_loc else losing_deck
    losing_deck = losing_deck[len(losing_cards):]
    wining_deck = wining_deck[len(wining_cards):] + wining_cards + losing_cards
    return wining_deck, losing_deck


def tie(player1_deck, player2_deck, recursion_num):
    tie_loc = 3 + (recursion_num * 3)
    player1_tie_card = player1_deck[tie_loc] if len(player1_deck) > tie_loc else player1_deck[-1]
    player2_tie_card = player2_deck[tie_loc] if len(player2_deck) > tie_loc else player2_deck[-1]
    if player1_tie_card > player2_tie_card:  # first player win
        player1_deck, player2_deck = tie_win(player1_deck, player2_deck, tie_loc)
    elif player1_tie_card < player2_tie_card:  # Second player win
        player2_deck, player1_deck = tie_win(player2_deck, player1_deck, tie_loc)
    else:  # tie
        recursion_num += 1
        # if recursion_num * 3 > min(len(player1_deck), len(player2_deck)):
        #     shuffle(player1_deck)
        #     shuffle(player2_deck)
        player1_deck, player2_deck = tie(player1_deck, player2_deck, recursion_num=recursion_num)
    return player1_deck, player2_deck


if __name__ == '__main__':
    iterations_nums = 1000
    recrusion_stop = 100
    max_iter = 5e4

    values_dic = {'1': 1,
                  '2': 2,
                  '3': 3,
                  '4': 4,
                  '5': 5,
                  '6': 6,
                  '7': 7,
                  '8': 8,
                  '9': 9,
                  '10': 10,
                  'J': 11,
                  'Q': 12,
                  'k': 13,
                  'Ace': 14,
                  'Joker': 15
                  }

    records = []
    results = []
    problematic_decks = []

    for iteration in range(iterations_nums):
        initial_deck = list(chain(*[[v] * 4 if k != 'Joker' else [v] * 2 for k, v in values_dic.items()]))
        shuffle(initial_deck)
        player1_deck = initial_deck[int(len(initial_deck) / 2):]
        player2_deck = initial_deck[:int(len(initial_deck) / 2)]
        step = 0
        while (len(player1_deck) != 0) and (len(player2_deck) != 0):
            step += 1
            player1_deck, player2_deck = game_step(player1_deck, player2_deck)
            records.append([iteration, step, len(player1_deck)])
            # print(iteration, step, len(player1_deck))
            if (len(player1_deck) == 0) or (len(player2_deck) == 0):
                results.append([iteration, step, len(player1_deck)])
                print(iteration, step, len(player1_deck))
            elif step % max_iter == 0:
                shuffle(player1_deck)
                shuffle(player2_deck)
                print('Shuffled due max iter', step, len(player1_deck), len(player2_deck))

    results_df = pd.DataFrame(results)
    results_df.columns = ['example_num', 'iter_num', 'step_to_conversion']
