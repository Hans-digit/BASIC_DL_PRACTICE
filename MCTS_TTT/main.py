# importing required libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pickle
import sys
from node import Node
import node
import time



# create a Window class
class Window(QMainWindow):
    # constructor
    def __init__(self, train_data):
        super().__init__()

        # setting title
        self.setWindowTitle("Tic Tac Toe AI ")

        # setting geometry
        self.setGeometry(100, 100,
                         300, 500)

        # calling method
        self.UiComponents(train_data)

        self.train_data = train_data
        # showing al
        # l the widgets
        self.show()

        self.first_turn = 0

    # method for components

    def UiComponents(self, train_data):

        # turn
        self.turn = 0

        # times
        self.times = 0

        # creating a push button list
        self.push_list = []

        self.push_hist = []

        # creating 2d list
        # for _ in range(3):
        for i in range(3):
            temp = []
            # for _ in range(3):
            for j in range(3):
                button = QPushButton(self)
                button.setObjectName(f'{i}_{j}')
                temp.append(button)
                # temp.append((QPushButton(self)))
            # adding 3 push button in single row
            self.push_list.append(temp)

        # x and y co-ordinate
        x = 90
        y = 90

        # traversing through push button list
        for i in range(3):
            for j in range(3):
                # setting geometry to the button
                self.push_list[i][j].setGeometry(x * j + 20,
                                                 y * i + 20,
                                                 80, 80)

                # setting font to the button
                self.push_list[i][j].setFont(QFont(QFont('Times', 17)))

                # adding action
                self.push_list[i][j].clicked.connect(lambda : self.action_called())

        # creating label to tel the score
        self.label = QLabel(self)

        # setting geometry to the label
        self.label.setGeometry(20, 360, 260, 50)

        # setting style sheet to the label
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid black;"
                                 "background : white;"
                                 "}")

        # setting label alignment
        self.label.setAlignment(Qt.AlignCenter)

        # setting font to the label
        self.label.setFont(QFont('Times', 15))

        # creating push button to restart the score
        reset_game = QPushButton("Reset-Game", self)

        # setting geometry
        reset_game.setGeometry(20, 420, 260, 50)

        # adding action action to the reset push button
        reset_game.clicked.connect(self.reset_game_action)
        #
        determine_first = QPushButton("I will do first",self)

        determine_first.setGeometry(20, 300, 130, 50)

        determine_first.clicked.connect(lambda: self.set_turn(0))

        determine_second = QPushButton("I will do second", self)

        determine_second.setGeometry(150, 300, 130, 50)

        determine_second.clicked.connect(lambda: self.set_turn(1))

    def set_turn(self, arg):
        self.reset_game_action()
        self.first_turn = arg

        print(self.first_turn)
        if self.first_turn == 1:
            self.action_called()

    # method called by reset button
    def reset_game_action(self):

        # resetting values
        self.turn = 0
        self.times = 0
        self.push_hist = []
        self.first_turn = 0
        # making label text empty:
        self.label.setText("")

        # traversing push list
        for buttons in self.push_list:
            for button in buttons:
                # making all the button enabled
                button.setEnabled(True)
                # removing text of all the buttons
                button.setText("")

    @staticmethod
    def _get_point_AI(push_hist, train_data):

        lower_node_list = train_data.next
        print('==================push hist ==============')
        print(push_hist)
        print('==========================================')
        if len(push_hist) == 0:
            print('push hist is None')
            prob_list = [(((i.win *2)+(i.draw)+(i.total-i.win-i.draw)*-3)  / i.total) for i in lower_node_list]
            print(prob_list)
            for i in lower_node_list:
                print(f'point : {i.point}, win : {i.win}, draw:{i.draw}, total:{i.total}')
            max_index = prob_list.index(max(prob_list))
            return lower_node_list[max_index].point
        else:
            for _ in range(len(push_hist)):
                node = [i for i in lower_node_list if i.point == push_hist[_]][0]
                lower_node_list = node.next
            prob_list = [(((i.win *2)+(i.draw)+(i.total-i.win-i.draw)*-3)  / i.total) for i in lower_node_list]
            print(prob_list)
            for i in lower_node_list:
                print(f'point : {i.point}, win : {i.win}, draw:{i.draw}, total:{i.total}')
            max_index = prob_list.index(max(prob_list))
            return lower_node_list[max_index].point


    # action called by the push buttons
    def action_called(self):

        self.times += 1

        # getting button which called the action
        person_turn = (self.turn == self.first_turn)
        AI_turn = (self.turn != self.first_turn)
        #

        if person_turn:
            button = self.sender()
            button.setEnabled(False)
            point = button.objectName().split('_')
            print('human point')
            print(point)
            point = [int(i) for i in point]
            if self.turn == 0:
                button.setText("O")
            else:
                button.setText("X")
            self.push_hist.append(point)
            self.turn = (self.turn + 1)%2

        else:
            point = self._get_point_AI(self.push_hist, self.train_data)
            print('ai point')
            print(point)
            button = self.push_list[point[0]][point[1]]
            button.setEnabled(False)
            if self.turn == 0:
                button.setText("O")
            else:
                button.setText("X")
            self.push_hist.append(point)
            self.turn = (self.turn + 1) % 2

        # call the winner checker method
        win = self.who_wins()


        # text
        text = ""

        # if winner is decided
        if win == True:
            # if current chance is 0
            if self.turn == 0:
                # O has won
                text = "X Won"
            # X has won
            else:
                text = "O Won"

            # disabling all the buttons
            for buttons in self.push_list:
                for push in buttons:
                    push.setEnabled(False)

        # if winner is not decided
        # and total times is 9
        elif self.times == 9:
            text = "Match is Draw"

        # setting text to the label
        self.label.setText(text)

        if person_turn:
            if self.times == 9:
                pass
            elif win is False:
                self.action_called()


    # method to check who wins
    def who_wins(self):

        # checking if any row crossed
        for i in range(3):
            if self.push_list[0][i].text() == self.push_list[1][i].text() \
                    and self.push_list[0][i].text() == self.push_list[2][i].text() \
                    and self.push_list[0][i].text() != "":
                return True

        # checking if any column crossed
        for i in range(3):
            if self.push_list[i][0].text() == self.push_list[i][1].text() \
                    and self.push_list[i][0].text() == self.push_list[i][2].text() \
                    and self.push_list[i][0].text() != "":
                return True

        # checking if diagonal crossed
        if self.push_list[0][0].text() == self.push_list[1][1].text() \
                and self.push_list[0][0].text() == self.push_list[2][2].text() \
                and self.push_list[0][0].text() != "":
            return True

        # if other diagonal is crossed
        if self.push_list[0][2].text() == self.push_list[1][1].text() \
                and self.push_list[1][1].text() == self.push_list[2][0].text() \
                and self.push_list[0][2].text() != "":
            return True

        # if nothing is crossed
        return False


with open('./model/TTT','rb') as f:
    train_data = pickle.load(f)

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window(train_data)

# start the app
sys.exit(App.exec())

