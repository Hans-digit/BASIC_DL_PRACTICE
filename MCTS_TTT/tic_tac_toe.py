import random
from loguru import logger
from node import Node
from math import log

LOGGER = logger

class TicTacToe():
    def __init__(self):
        ''

    def set_first_node(self):
        first_node = Node()
        for i in range(3):
            for j in range(3):
                second_node = Node(first_node)
                second_node.point = [i, j]
                first_node.next.append(second_node)
        return first_node

    def update_node(self, target_node, winner):
        prev_node_list = []
        while target_node.prev is not None:
            prev_node_list.append(target_node)
            target_node = target_node.prev
        prev_node_list = prev_node_list[::-1]
        target_node.total += 1
        # print('befor update')
        # prev_node_list_test = list(prev_node_list)
        # prev_node_list_test = prev_node_list_test[::-1]
        # for node in prev_node_list_test:
        #     print(node.total)
        #     print(node.win)

        # print(f'len prev_node_list : {len(prev_node_list)}')
        if winner == 'white':
            for i in range(len(prev_node_list)):
                if i % 2 == 0:
                    prev_node_list[i].win += 1
                    prev_node_list[i].total += 1
                else:
                    prev_node_list[i].total += 1
        elif winner == 'black':
            for i in range(len(prev_node_list)):
                if i % 2 == 0:
                    prev_node_list[i].total += 1
                else:
                    prev_node_list[i].win += 1
                    prev_node_list[i].total += 1
        else:
            for i in range(len(prev_node_list)):
                prev_node_list[i].total += 1
                # LOGGER.info('darw game')

        # prev_node_list_test = list(prev_node_list)
        # prev_node_list_test = prev_node_list_test[::-1]
        # for node in prev_node_list_test:
        #     print(node.total)
        #     print(node.win)

    def start_fight(self, target_node, referee):
        white_list, black_list, prev_list= self._return_each_list(target_node)
        total_point = [[i, j] for i in range(3) for j in range(3)]
        left_point = [i for i in total_point if i not in prev_list]
        winner = self._random_fight(white_list, black_list, left_point, referee)
        return winner

    def _return_each_list(self, target_node):
        white_list = []
        black_list = []
        prev_list = self._get_prev_list(target_node)
        prev_list = prev_list[::-1]
        total_point = [[i, j] for i in range(3) for j in range(3)]

        # LOGGER.info(f'total point is {total_point}')
        # LOGGER.info(f'left point is {left_point}')
        # LOGGER.info(f'prev list is {prev_list}')
        for i in range(len(prev_list)):
            if i % 2 == 0:
                white_list.append(prev_list[i])
                # LOGGER.info(f'white put {white_list}')
            else:
                black_list.append(prev_list[i])
                # LOGGER.info(f'black put {black_list}')
        return white_list, black_list, prev_list

    @staticmethod
    def _random_fight(white_list, black_list, left_point, referee):
        winner = 'draw'
        random.shuffle(left_point)
        for _ in left_point:
            if len(white_list) == len(black_list):
                white_list.append(_)
                # LOGGER.info(f'white put {white_list}')
                if referee.check_end(white_list) is True:
                    winner = 'white'
                    break
            else:
                black_list.append(_)
                # LOGGER.info(f'black put {black_list}')
                if referee.check_end(black_list) is True:
                    winner = 'black'
                    break
        return winner


    def start_depth(self, target_node):
        prev_list = self._get_prev_list(target_node)
        self._create_lower_node(target_node, prev_list)

    @staticmethod
    def _create_lower_node(target_node, prev_list):
        total_point = [[i, j] for i in range(3) for j in range(3)]
        left_point = [i for i in total_point if i not in prev_list]
        if len(left_point) == 0:
            return None
        else:
            for point in left_point:
                lower_node = Node(target_node)
                lower_node.point = point
                target_node.next.append(lower_node)

    @staticmethod
    def _get_prev_list(target_node):
        prev_list = []
        while target_node.point is not None:
            prev_list.append(target_node.point)
            target_node = target_node.prev
        return prev_list

    @staticmethod
    def cal_ucb(node_upper):
        total_cnt = 0
        lower_node_list = node_upper.next
        if len(lower_node_list) == 0:
            return None
        else:
            for lower_node in lower_node_list:
                total_cnt += lower_node.total
        if total_cnt == 0:
            return 'random'
        ucb_list = []
        for lower_node in lower_node_list:
            # ucb = (lower_node.win / (lower_node.total + (1e-10))) + pow(
            #     (2 * log(total_cnt) / (lower_node.total + (1e-10))),
            #     1 / 2)
            ucb = pow((2 * total_cnt / (lower_node.total + (1e-10))),1 / 2)
            ucb_list.append(ucb)
        max_index = ucb_list.index(max(ucb_list))
        return lower_node_list[max_index]


