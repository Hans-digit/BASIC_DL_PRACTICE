from operator import itemgetter

class Referee():
    def __init__(self):
        print('')

    # def check_impossible_point(self, point):

    #
    #
    # def _get_33_point(self):
    #
    # def _get_3_count(self, target_point, stone_list):
    #     count = 0
    #     self._get_3_vertical_count

    def end_check(self, stone_list):
        result = False
        result = result or self._check_5_horizontal_end(stone_list)
        result = result or self._check_5_vertical_end(stone_list)
        result = result or self._check_5_up_right_diagonal_end(stone_list)
        result = result or self._check_5_down_right_diagonal_end(stone_list)
        return result

    @staticmethod
    def _check_5_horizontal_end(stone_list):
        stone_list_data = list(stone_list)
        stone_list_data = sorted(stone_list_data, key = itemgetter(0, 1))
        # print(stone_list_data)
        count = 0
        for i in range(len(stone_list_data)):
            try:
                if set([stone_list_data[i][0], stone_list_data[i][1] + 1]) == set(stone_list_data[i+1]):
                    count += 1
                else:
                    count = 0
                if count == 4:
                    # print('horizontal end success')
                    return True
            except:
                return False

        return False

    @staticmethod
    def _check_5_vertical_end(stone_list):
        stone_list_data = list(stone_list)
        stone_list_data = sorted(stone_list_data, key=itemgetter(1, 0))
        count = 0
        for i in range(len(stone_list_data)):
            try:
                if set([stone_list_data[i][0] +1, stone_list_data[i][1]]) == set(stone_list_data[i + 1]):
                    count += 1
                else:
                    count = 0
                if count == 4:
                    # print('vertical end success')
                    return True
            except:
                return False

        return False

    @staticmethod
    def _check_5_up_right_diagonal_end(stone_list):
        stone_list_data = list(stone_list)
        stone_list_data = sorted(stone_list_data, key=itemgetter(1, 0))
        count = 0
        stone_list_result = []
        for i in range(len(stone_list_data)):
            first_stone = stone_list_data[i]
            while True:
                if [first_stone[0] - 1, first_stone[1] +1] in stone_list_data:
                    stone_list_result.append(first_stone)
                    first_stone = list([first_stone[0] -1, first_stone[1] +1])
                    count += 1
                else:
                    count = 0
                    stone_list_result = []
                    break
                if count == 4:
                    # print(stone_list_result + [first_stone])
                    # print('up right end success')
                    return True
        return False

    @staticmethod
    def _check_5_down_right_diagonal_end(stone_list):
        stone_list_data = list(stone_list)
        stone_list_data = sorted(stone_list_data, key=itemgetter(1, 0))
        count = 0
        for i in range(len(stone_list_data)):
            first_stone = stone_list_data[i]
            while True:
                if [first_stone[0] + 1, first_stone[1] + 1] in stone_list_data:
                    first_stone = list([first_stone[0] + 1, first_stone[1] + 1])
                    count += 1
                else:
                    count = 0
                    break
                if count == 4:
                    # print('down right end success')
                    return True
        return False


    def _move_point(self, point, direction, amount):
        result = list(point)
        if direction == 'up':
            result = [result[0] -amount, result[1]]
            return result
        elif direction == 'down':
            result = [result[0] + amount, result[1]]
            return result
        elif direction == 'right':
            result = [result[0], result[1] + amount]
            return result
        elif direction == 'left':
            result = [result[0], result[1] - amount]
            return result
        elif direction == 'up_right':
            result = [result[0] - amount, result[1] + amount]
            return result
        elif direction == 'up_left':
            result = [result[0] - amount, result[1] - amount]
            return result
        elif direction == 'down_right':
            result = [result[0] + amount, result[1] + amount]
            return result
        elif direction == 'down_left':
            result = [result[0] + amount, result[1] - amount]
            return result
        else:
            return result

    def _check_occupied_point(self, target_point, stone_list, stone_list_opponent):
        if target_point in stone_list + stone_list_opponent:
            return True
        else:
            return False

    def check_3_count(self, target_point, stone_list, stone_list_opponent):
        if self._check_occupied_point(target_point, stone_list, stone_list_opponent):
            # print(f'already ocuupied point {target_point}')
            return True
        vertical_count = self._check_3_direction_count('up', 'down', target_point, stone_list, stone_list_opponent)
        # print(f'vertical count {vertical_count}')
        horizontal_count = self._check_3_direction_count('right', 'left', target_point, stone_list, stone_list_opponent)
        # print(f'horizontal_count {horizontal_count}')
        up_right_diagonal_count = self._check_3_direction_count('up_right', 'down_left', target_point, stone_list, stone_list_opponent)
        # print(f'up_right diagonal count {up_right_diagonal_count}')
        down_right_diagonal_count = self._check_3_direction_count('down_right', 'up_left', target_point, stone_list, stone_list_opponent)
        # print(f'down_right diagonal count {down_right_diagonal_count}')
        if vertical_count + horizontal_count + up_right_diagonal_count + down_right_diagonal_count >= 2:
            return True
        else:
            return False

    def _check_3_direction_count(self, direction1, direction2, target_point, stone_list, stone_list_opponent):
        count = 0
        if self._move_point(target_point, direction1, 1) in stone_list:
            if self._move_point(target_point, direction1, 2) in stone_list:
                if self._move_point(target_point, direction1, 3) in stone_list:
                    pass
                elif self._move_point(target_point, direction1, 4) in stone_list:
                    pass
                elif self._move_point(target_point, direction2, 1) in stone_list:
                    pass
                elif self._move_point(target_point, direction2, 2) in stone_list:
                    pass
                else:
                    count += 1
            else:
                if self._move_point(target_point, direction1, 3) in stone_list:
                    if self._move_point(target_point, direction1, 4) in stone_list:
                        pass
                    elif self._move_point(target_point, direction2, 1) in stone_list:
                        pass
                    elif self._move_point(target_point, direction2, 1) in stone_list_opponent:
                        pass
                    else:
                        count += 1
                else:
                    pass

        if self._move_point(target_point, direction2, 1) in stone_list:
            if self._move_point(target_point, direction2, 2) in stone_list:
                if self._move_point(target_point, direction2, 3) in stone_list:
                    pass
                elif self._move_point(target_point, direction2, 4) in stone_list:
                    pass
                elif self._move_point(target_point, direction1, 1) in stone_list:
                    pass
                elif self._move_point(target_point, direction1, 2) in stone_list:
                    pass
                else:
                    count += 1
            else:
                if self._move_point(target_point, direction2, 3) in stone_list:
                    if self._move_point(target_point, direction2, 4) in stone_list:
                        pass
                    elif self._move_point(target_point, direction1, 1) in stone_list:
                        pass
                    elif self._move_point(target_point, direction1, 1) in stone_list_opponent:
                        pass
                    else:
                        count += 1
                else:
                    pass

        if self._move_point(target_point, direction1, 1) in stone_list:
            if self._move_point(target_point, direction2, 1) in stone_list:
                if self._move_point(target_point, direction1, 2) in stone_list:
                    pass
                elif self._move_point(target_point, direction1, 3) in stone_list:
                    pass
                elif self._move_point(target_point, direction2, 2) in stone_list:
                    pass
                elif self._move_point(target_point, direction2, 3) in stone_list:
                    pass
                elif self._move_point(target_point, direction1, 2) in stone_list_opponent:
                    pass
                elif self._move_point(target_point, direction2, 2) in stone_list_opponent:
                    pass
                else:
                    count += 1

        return count


if __name__=='__main__':
    print('test start')
    referee = Referee()


    print('='*10+'test 1 : 3 point test ' + '='*10)
    target_point = [4,4]
    stone_list = [[3,4],[5,4]]
    opponent_list = [[2,4]]
    print(f'target : {target_point} , stone_list : {stone_list}, opponent_list : {opponent_list}')
    total_count = referee.check_3_count(target_point, stone_list, opponent_list)
    print(f'total_count : {total_count}')

    target_point = [4, 4]
    stone_list = [[3, 4], [5, 4]]
    opponent_list = [[1, 4]]
    print(f'target : {target_point} , stone_list : {stone_list}, opponent_list : {opponent_list}')
    total_count = referee.check_3_count(target_point, stone_list, opponent_list)
    print(f'total_count : {total_count}')

    target_point = [4, 4]
    stone_list = [[3, 4], [5, 4], [7,4]]
    opponent_list = [[1, 4]]
    print(f'target : {target_point} , stone_list : {stone_list}, opponent_list : {opponent_list}')
    total_count = referee.check_3_count(target_point, stone_list, opponent_list)
    print(f'total_count : {total_count}')

    print('=' * 10 + 'test 2 : 5 point test ' + '=' * 10)
    print('horizontal check')
    print('true case')
    stone_list = [[0,1],[0,2],[0,3],[1,2],[0,4],[6,6],[0,5]]
    print(f'stone_list : {stone_list}')
    print(referee.end_check(stone_list))
    print('false case')
    stone_list = [[0, 1], [0, 2], [0, 3], [1, 2], [0, 4], [6, 6], [2,2],[3,2],[4,2],[7,6],[1,2]]
    print(f'stone_list : {stone_list}')
    print(referee.end_check(stone_list))
    print('vertical check')
    stone_list = [[2,2],[3,2],[4,2],[7,6],[1,2]]
    print(f'stone_list : {stone_list}')
    print(referee.end_check(stone_list))

    print('up right check')
    stone_list = [[5,5],[7,4],[4,5],[6,7],[4,6],[3,7],[2,8],[6,4]]
    print(f'stone_list : {stone_list}')
    print(referee.end_check(stone_list))

    print('error test')
    stone_list = [[2, 9], [1, 7], [13, 3], [12, 9], [2, 10], [0, 4], [10, 13], [0, 2], [0, 3], [13, 6], [7, 10], [9, 3], [9, 6], [11, 10], [9, 10], [6, 3], [10, 8], [11, 0], [3, 2], [11, 4], [9, 14], [6, 5], [9, 7], [10, 9], [14, 13], [6, 6], [13, 5], [10, 11], [7, 14], [3, 6], [9, 12], [12, 13], [7, 1], [14, 0], [4, 11], [2, 13], [6, 0], [13, 9], [8, 9], [10, 5], [7, 9], [0, 14], [1, 2], [8, 13]]
    print(f'stone_list : {stone_list}')
    print(referee.end_check(stone_list))



