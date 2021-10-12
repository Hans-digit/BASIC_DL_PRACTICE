class Node:
    def __init__(self, prev = None) -> None:
        self.next = []
        self.prev = prev
        self.point = None
        self.win = 0
        self.total = 0
        self.draw = 0