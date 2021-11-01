import torch
import time
import torch.nn.functional as F
import numpy as np

"""
model based on Mastering the game of go without human ... 

"""

class CNN_Gomoku(torch.nn.Module):
    def __init__(self):
        super(CNN_Gomoku, self).__init__()

        # first layer
        # in size : 16 * 12 * 15 * 15
        # conv size : 16 * 24 * 16 * 16
        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv2d(12, 24, kernel_size=4, stride=1, padding=2),
            torch.nn.ReLU())


        # second layer
        # in size : 24 * 24 * 16 * 16
        # conv size : 24 * 24 * 15 * 15
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=4, stride=1, padding=1),
            torch.nn.ReLU())

        # third layer
        # in size : 24 * 24 * 15 * 15
        # conv size : 24 * 24 * 14 * 14
        # pool size : 24 * 24 * 13 * 13
        self.layer3 = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=4, stride=1, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=1))

        # fourth layer
        # in size : 24 * 24 * 13 * 13
        # conv size : 24 * 24 * 12 * 12
        self.layer4 = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=4, stride=1, padding=1),
            torch.nn.ReLU())

        # fifth layer
        # in size : 24 * 24 * 12 * 12
        # conv size : 24 * 24 * 11 * 11
        self.layer5 = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=4, stride=1, padding=1),
            torch.nn.ReLU())

        # sixth layer
        # in size : 24 * 24 * 11 * 11
        # conv size : 24 * 24 * 10 * 10
        self.layer6 = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=4, stride=1, padding=1),
            torch.nn.ReLU())


        self.fc = torch.nn.Linear(24 * 10 * 10, 225 + 1)




        torch.nn.init.xavier_uniform_(self.fc.weight)


    def forward(self, batch_gomoku_tensor, batch_size):
        out = self.layer1(batch_gomoku_tensor)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = self.layer6(out)
        out = out.view([batch_size, -1])
        out = self.fc(out)


        return out

    def get_top10(self, batch_gomoku_tensor):
        out = self.layer1(batch_gomoku_tensor)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = self.layer6(out)
        out = out.view([1, -1])
        out = self.fc(out)
        out = torch.topk(out, 200)
        return out




