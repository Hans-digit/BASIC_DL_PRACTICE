"""
바둑은 흑이 먼저
"""
"""
아이디어: 
CNN 으로 다음의 수를 예측할때, 누구의 수가 예측되는가 ? 

이렇게 하도록 하자 
필터종류 

첫번째 필터 - 예측하고자 하는 것 
두번째 필터 - 상대방 
세번째 ~ 7번째 필터 - 내가 최근 5번 둔 것 
여덟번째 ~ 12번째 필터 - 내가 최근 5번 둔 것 

예측 - 첫번째 필터를 둔 것이 다음에 두고싶은 수 
"""
import torch

class Gomoku():

    def __init__(self):
        self.gomoku_dim = 15
        print('')


    def _get_zero_stage(self):
        return torch.FloatTensor([[[0 for i in range(self.gomoku_dim)] for j in range(self.gomoku_dim)]])

    def gomoku_to_tensor(self, stone_list_target, stone_list_opponent):
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
            tensor_target[stone_target[0], stone_target[1]] = 1
        for stone_opponent in stone_list_opponent:
            tensor_opponent[stone_opponent[0], stone_opponent[1]] = 1

        try:
            tensor_target_bf_0[stone_list_target[-1][0], stone_list_target[-1][1]] = 1
            tensor_target_bf_1[stone_list_target[-2][0], stone_list_target[-2][1]] = 1
            tensor_target_bf_2[stone_list_target[-3][0], stone_list_target[-3][1]] = 1
            tensor_target_bf_3[stone_list_target[-4][0], stone_list_target[-4][1]] = 1
            tensor_target_bf_4[stone_list_target[-5][0], stone_list_target[-5][1]] = 1
        except:
            pass

        try:
            tensor_opponent_bf_0[stone_list_opponent[-1][0], stone_list_opponent[-1][1]] = 1
            tensor_opponent_bf_1[stone_list_opponent[-2][0], stone_list_opponent[-2][1]] = 1
            tensor_opponent_bf_2[stone_list_opponent[-3][0], stone_list_opponent[-3][1]] = 1
            tensor_opponent_bf_3[stone_list_opponent[-4][0], stone_list_opponent[-4][1]] = 1
            tensor_opponent_bf_4[stone_list_opponent[-5][0], stone_list_opponent[-5][1]] = 1
        except:
            pass

        result_tensor = torch.cat((tensor_target, tensor_opponent,
                                   tensor_target_bf_0, tensor_target_bf_1, tensor_target_bf_2, tensor_target_bf_3, tensor_target_bf_4,
                                   tensor_opponent_bf_0, tensor_opponent_bf_1, tensor_opponent_bf_2, tensor_opponent_bf_3, tensor_opponent_bf_4), dim = 1)

        return result_tensor


