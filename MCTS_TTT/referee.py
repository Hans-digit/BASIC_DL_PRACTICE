from operator import itemgetter

class Referee:
    def __init__(self):
        self.white = []
        self.black = []
        self.total = []

    def check_end(self, data):
        result = self._check_horizontal_end(data)
        result = result or self._check_vertical_end(data)
        result = result or self._check_diagonal_end(data)
        return result

    @staticmethod
    def _check_horizontal_end(data):
        count = 0
        get_data = list(data)
        get_data = sorted(get_data, key=itemgetter(0, 1))
        for i in range(len(get_data) - 1):
            if get_data[i + 1][0] == get_data[i][0]:
                count += 1
                if count == 2:
                    return True
                else:
                    pass
            else:
                count = 0
        return False

    @staticmethod
    def _check_vertical_end(data):
        get_data = list(data)
        get_data = sorted(get_data, key=itemgetter(1, 0))
        count = 0
        for i in range(len(get_data) - 1):
            if get_data[i + 1][1] == get_data[i][1]:
                count += 1
                if count == 2:
                    return True
                else:
                    pass
            else:
                count = 0
        return False

    @staticmethod
    def _check_diagonal_end(data):
        count = 0
        for _ in range(3):
            if [_, _] in data:
                count += 1
            else:
                pass
        if count == 3:
            return True

        count = 0
        for _ in range(3):
            if [2 - _, _] in data:
                count += 1
            else:
                pass
        if count == 3:
            return True

        return False