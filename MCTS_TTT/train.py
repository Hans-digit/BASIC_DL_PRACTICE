from typing import Any, Type
import random
import time
from loguru import logger
from operator import itemgetter
from math import log
from node import Node
from referee import Referee
from tic_tac_toe import TicTacToe
import pickle
from tqdm import tqdm

LOGGER = logger

def train(count_limit, mode='first', first_node=None):
    count = 0
    nth_limit = 0
    tictactoe = TicTacToe()

    # LOGGER.info('get referee')
    referee = Referee()
    # LOGGER.success('got referee')

    if mode == 'first':
        # LOGGER.info('mode is first')
        first_node = tictactoe.set_first_node()
    else:
        # LOGGER.info('use saved first node')
        first_node = first_node
    while count < count_limit:
        if count%10000==0:
            print('='*20)
            print(count)
            print('=' * 20)
        target_node = first_node
        cnt = 0
        depth = 0
        while True:
            # LOGGER.info('calculate ucb')
            target = tictactoe.cal_ucb(target_node)

            #
            # check whether now it is end or not for every turn
            #
            if target is None:
                # LOGGER.info('target is None')
                white_list, black_list, prev_list = tictactoe._return_each_list(target_node)
                # LOGGER.info(f'{white_list},{black_list},{prev_list}')
                if referee.check_end(white_list):
                    tictactoe.update_node(target_node, 'white')
                    count += 1
                    break
                elif referee.check_end(black_list):
                    # print('BLACK WIN!!!='*10)
                    tictactoe.update_node(target_node, 'black')
                    count += 1
                    break
                else:
                    if len(prev_list) == 9:
                        tictactoe.update_node(target_node, 'draw')
                        count += 1
                        break
                    else:
                        pass

            #
            # if it is not the end
            # (i) first, expand the tree
            # (ii) or reach for the end
            #

            if target is None:
                # LOGGER.info('next node is None')
                if target_node.total >= nth_limit:
                    # LOGGER.info('start depth process')
                    tictactoe.start_depth(target_node)
            else:
                if target == 'random':
                    # LOGGER.info('ucb result is random, so choice random one')
                    target = random.choice(target_node.next)
                    target_node = target
                else:
                    # LOGGER.info('reach for the last one')
                    target_node = target
    return first_node


def main():
    first_node = train(100000000)
    with open('./model/TTT', 'wb') as f:
        pickle.dump(first_node,f)


if __name__=='__main__':
    main()