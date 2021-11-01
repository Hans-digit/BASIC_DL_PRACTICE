"""
based on the article

mastering the game of Go without human knowledge
"""
import torch
import random
from referee import Referee
import math

class Gomoku():

    def __init__(self):
        self.gomoku_dim = 15
        self.all_remain_states = [[i,j] for i in range(15) for j in range(15)]


    def _get_zero_stage(self):
        return torch.FloatTensor([[[[0 for i in range(self.gomoku_dim)] for j in range(self.gomoku_dim)]]])

    def show_state(self, black_stone_list, white_stone_list):
        plate = self._get_zero_stage()
        for _ in black_stone_list:
            plate[0, 0, _[0], _[1]] = 1
        for _ in white_stone_list:
            plate[0, 0, _[0], _[1]] = 2
        return plate

    def get_first_move(self, stone_list_target, stone_list_opponent, target_move_history_list, target_move_count_list):
        remain_states = self.get_remain_states(stone_list_target, stone_list_opponent)
        unreached_states = list(set(remain_states) - set(target_move_history_list))
        if len(unreached_states) != 0:
            result = 'unreached'
            return result, random.choice(unreached_states)
        else:
            result = 'reached'
            move_probability = self._get_first_move_probability(target_move_count_list)
            first_move = random.choices(population=target_move_history_list,
                                        weights=move_probability, k=1)
            return result, first_move

    @staticmethod
    def _get_first_move_probability(move_count_list, tau = 1):
        move_count_list = [math.pow(i, 1/tau) for i in move_count_list]
        move_count_list = [i/sum(move_count_list) for i in move_count_list]
        return move_count_list


    def get_nth_move(self, stone_list_target, stone_list_opponent, move_history, move_possibilities, target_stone_color):
        '''
        :param stone_list_target:
        :param stone_list_opponent:
        :param move_history:
        :param move_possibilities:
        :param target_stone_color:
        :return:

         return data which target player should pick
         it uses Q and U functions
         Q function : use state value data
         U function : use frequency data
        '''
        # get all possible points
        remain_states = self.get_remain_states(stone_list_target, stone_list_opponent)
        max_state = None
        max_state_value = 0
        if target_stone_color is 'black':
            # for each remain states, calculate Q and U function
            for state in remain_states:
                # calculate q + u
                Q_value = self._cal_Q_value()
                U_value = self._cal_U_value()
                pi_value = Q_value + U_value
                if max_state_value > pi_value:
                    max_state_value = pi_value
                    max_state = state




        else:

    @staticmethod
    def _cal_Q_value(stone_list_target, stone_list_opponent, move_history, target_state):


    @staticmethod
    def _cal_U_value(stone_list_target, stone_list_opponent, move_history, move_possibilities, target_state, const):







        # act ( not on probability but exact argmax )

    @staticmethod
    def update_state_value(move_history, move_list, state_value, start_stone_color):
        '''
        :param move_history:
            put history data, data form is [[{black_stone_set},{white_stone_set},count,value],...,[]]
        :param move_list:
            1 mcts move list data, data for is
                if black is first, [ black stone position, white stone position, black stone position, ... , ]
                if white is first, [ white stone position, black stone position, white stone position, ... , ]
        :param state_value:
            state_value is last leaf value
        # :param start_stone_color:
        #     start_stone_color is string data which explain start stone color of move_list ( 'black' or 'white' )
        :return:
            return is updated - move_history

        if move_list = [b1 w1 b2 w2 b3]
        [{b1}{}], [{b1}{w1}], [{b1 b2}{w1}], [{b1 b2}{w1 w2}]
        if move_list = [b1 w1 b2 w2]
        [{b1}{}], [{b1}{w1}], [{b1 b2}{w1}]

        if move_list = [w1 b1 w2 b2 w3]
        [{}{w1}], [{b1}{w1}], [{b1}{w1 w2}], [{b1 b2}{w1 w2}]
        if move_list = [w1 b1 w2 b2]
        [{}{w1}], [{b1}{w1}], [{b1}{w1 w2}]
        '''

        if start_stone_color is 'black':
            target_set_list = []
            temp_list = [set(), set()]
            for list_index in range(len(move_list)-1):
                if list_index%2 == 0:
                    temp_list[0].add(move_list[list_index])
                    target_set_list.append(temp_list)
                else:
                    temp_list[1].add(move_list[list_index])
                    target_set_list.append(temp_list)

            for target_data in target_set_list:
                for history_index in range(len(move_history)):
                    if target_data[0] == move_history[history_index][0]:
                        if target_data[1] == move_history[history_index][1]:
                            move_history_value = move_history[history_index][2]*move_history[history_index][3] + state_value
                            move_history_cnt = move_history[history_index][2]+1
                            move_history[history_index][2] = move_history_cnt
                            move_history[history_index][3] = move_history_value / move_history_cnt
                            break
            return move_history

        else:
            target_set_list = []
            temp_list = [set(), set()]
            for list_index in range(len(move_list) - 1):
                if list_index % 2 == 0:
                    temp_list[1].add(move_list[list_index])
                    target_set_list.append(temp_list)
                else:
                    temp_list[0].add(move_list[list_index])
                    target_set_list.append(temp_list)

            for target_data in target_set_list:
                for history_index in range(len(move_history)):
                    if target_data[0] == move_history[history_index][0]:
                        if target_data[1] == move_history[history_index][1]:
                            move_history_value = move_history[history_index][2] * move_history[history_index][3] + state_value
                            move_history_cnt = move_history[history_index][2] + 1
                            move_history[history_index][2] = move_history_cnt
                            move_history[history_index][3] = move_history_value / move_history_cnt
                            break
            return move_history




    @staticmethod
    def random_put(random_probability):
        random_number = random.uniform(0, 1)
        return random_number < random_probability

    @staticmethod
    def random_point(stone_list_target, stone_list_opponent):
        total_point = [[i,j] for i in range(15) for j in range(15)]
        total_point = [i for i in total_point if i not in stone_list_target]
        total_point = [i for i in total_point if i not in stone_list_opponent]
        random_point = random.choice(total_point)
        return random_point

    def get_remain_states(self, stone_list_target, stone_list_opponent):
        """
        :param stone_list_target: get all stone list of target player
        :param stone_list_opponent: get all stone list of opponent player
        :return: return all remaining stone positions
        """
        all_remain_states = []
        referee = Referee()
        for i in self.all_remain_states:
            if i in stone_list_target + stone_list_opponent:
                pass
            elif referee.check_3_count(i, stone_list_target, stone_list_opponent):
                pass
            else:
                all_remain_states.append(i)
        return all_remain_states

    def get_gomoku_to_tensor(self, stone_list_target, stone_list_opponent):
        return self._gomoku_to_tensor(stone_list_target, stone_list_opponent)

    def _gomoku_to_tensor(self, stone_list_target, stone_list_opponent):
        """
        :param stone_list_target: stone data which you want to predict,  dim : 1 * 1 * 15 * 15
        :param stone_list_opponent: stone data which is opponent to target, dim : 1 * 1 * 15 * 15
        :return: two target added data + add before channel (10) , dim : 1 * 12 * 15 * 15
        """
        result_tensor = None
        tensor_target = self._get_zero_stage()
        tensor_opponent = self._get_zero_stage()

        tensor_target_bf_0 = self._get_zero_stage()
        tensor_target_bf_1 = self._get_zero_stage()
        tensor_target_bf_2 = self._get_zero_stage()
        tensor_target_bf_3 = self._get_zero_stage()
        tensor_target_bf_4 = self._get_zero_stage()

        tensor_opponent_bf_0 = self._get_zero_stage()
        tensor_opponent_bf_1 = self._get_zero_stage()
        tensor_opponent_bf_2 = self._get_zero_stage()
        tensor_opponent_bf_3 = self._get_zero_stage()
        tensor_opponent_bf_4 = self._get_zero_stage()

        for stone_target in stone_list_target:
            tensor_target[0, 0, stone_target[0], stone_target[1]] = 1
        for stone_opponent in stone_list_opponent:
            tensor_opponent[0, 0, stone_opponent[0], stone_opponent[1]] = 1

        try:
            tensor_target_bf_0[0, 0, stone_list_target[-1][0], stone_list_target[-1][1]] = 1
            tensor_target_bf_1[0, 0, stone_list_target[-2][0], stone_list_target[-2][1]] = 1
            tensor_target_bf_2[0, 0, stone_list_target[-3][0], stone_list_target[-3][1]] = 1
            tensor_target_bf_3[0, 0, stone_list_target[-4][0], stone_list_target[-4][1]] = 1
            tensor_target_bf_4[0, 0, stone_list_target[-5][0], stone_list_target[-5][1]] = 1
        except:
            pass

        try:
            tensor_opponent_bf_0[0, 0, stone_list_opponent[-1][0], stone_list_opponent[-1][1]] = 1
            tensor_opponent_bf_1[0, 0, stone_list_opponent[-2][0], stone_list_opponent[-2][1]] = 1
            tensor_opponent_bf_2[0, 0, stone_list_opponent[-3][0], stone_list_opponent[-3][1]] = 1
            tensor_opponent_bf_3[0, 0, stone_list_opponent[-4][0], stone_list_opponent[-4][1]] = 1
            tensor_opponent_bf_4[0, 0, stone_list_opponent[-5][0], stone_list_opponent[-5][1]] = 1
        except:
            pass

        result_tensor = torch.cat((tensor_target, tensor_opponent,
                                   tensor_target_bf_0, tensor_target_bf_1, tensor_target_bf_2, tensor_target_bf_3, tensor_target_bf_4,
                                   tensor_opponent_bf_0, tensor_opponent_bf_1, tensor_opponent_bf_2, tensor_opponent_bf_3, tensor_opponent_bf_4), dim = 1)

        return result_tensor


