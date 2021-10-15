import torch
import time
import torch.nn.functional as F
import numpy as np

"""
model ->    1. cnn + linear + linear ( win or lose )
                -> can use 'win' and 'lose' data both
                -> to get the next point, it should calculate every single point's win probability
            2. cnn + linear ( which point )
                -> cannot use 'lose' data
"""

class CNN_Gomoku(torch.nn.Module):
    def __init__(self):
        super(CNN_Gomoku, self).__init__()

        # first layer
        # in size : 16 * 12 * 15 * 15
        # conv size : 16 * 24 * 14 * 14
        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv2d(12, 24, kernel_size=4, stride=1, padding=1),
            torch.nn.ReLU())

        # second layer
        # in size : 24 * 24 * 14 * 14
        # conv size : 24 * 24 * 14 * 14
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=4, stride=1, padding=2),
            torch.nn.ReLU())

        # third layer
        # in size : 24 * 24 * 14 * 14
        # conv size : 24 * 24 * 14 * 14
        # pool size : 24 * 24 * 13 * 13
        self.layer3 = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=4, stride=1, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=1))

        # fourth layer
        # in size : 24 * 24 * 13 * 13
        # conv size : 24 * 24 * 12 * 12
        self.layer4 = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=4, stride=1, padding=1),
            torch.nn.ReLU())

        self.fc = torch.nn.Linear(24 * 12 * 12, 225)

        torch.nn.init.xavier_uniform_(self.fc.weight)

    def forward(self, batch_gomoku_tensor):
        out = self.layer1(batch_gomoku_tensor)
        out = self.layer2(batch_gomoku_tensor)
        out = self.layer3(batch_gomoku_tensor)
        out = self.layer4(batch_gomoku_tensor)
        out = self.fc(out)
        return out




