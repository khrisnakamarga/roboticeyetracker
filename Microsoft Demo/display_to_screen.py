import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt

class MockCalibration(QWidget):

    def __init__(self):
        # # willie's screen
        # self.screenx = 1920
        # self.screeny = 1080

        # # khrisna's screen
        # self.screenx = 3840
        # self.screeny = 2160

        # kai's screen
        self.screenx = 2560
        self.screeny = 1440

        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, self.screenx, self.screeny)
        self.setWindowTitle('Mock Calibration Screen')
        self.setStyleSheet("background-color: black")
        self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))


        # painter.drawEllipse(self.screenx/8, self.screeny/6, 50, 50)
        # painter.drawEllipse(self.screenx *1/2, self.screeny/6, 50, 50)
        # painter.drawEllipse(self.screenx *7/8, self.screeny/6, 50, 50)
        #
        #
        # painter.drawEllipse(self.screenx/8, self.screeny *5/6, 50, 50)
        # painter.drawEllipse(self.screenx *1/2, self.screeny *5/6, 50, 50)
        # painter.drawEllipse(self.screenx *7/8, self.screeny *5/6, 50, 50)

        ## DRAWING A SQUARE
        painter.setPen(QPen(Qt.blue, 50, Qt.SolidLine))
        # length = 300
        # startx = 1097 # between 0 to screenlength - length (2560 - length)
        # starty = 576 # between 0 to screenheight - length (1440 - length)
        #
        # painter.drawLine(startx, starty, startx, starty + length)
        # painter.drawLine(startx + length, starty, startx + length, starty + length)
        # painter.drawLine(startx, starty + length, startx + length, starty + length)
        # painter.drawLine(startx, starty, startx + length, starty)


        ## CALIBRATION GRID DOTS
        #before: 5 rows, 16 columns
        painter.setPen(QPen(Qt.blue, 8, Qt.SolidLine))
        for row in range(4):
            for col in range(6):
                print('\ncol:', self.screenx * (col + 1) / 11, 'row', self.screeny * (row + 1) / 5)
                painter.drawEllipse(self.screenx * (col + 1) / 7, self.screeny * (row + 1) / 5, 50, 50)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MockCalibration()
    sys.exit(app.exec_())


######################################################################################################################
# OLD GRAPHICS
######################################################################################################################

# from graphics import *
#
# # creates a 1366 x 768 black window (EASY TO CHANGE) and
# # draws a 3 x 2 grid of blue dots equally spaced.
# # clicking the screen will close program.
# def display_to_screen():
#     # background size and color
#     # 16:9 aspect ratio window size
#     screenx = 1366
#     screeny = 768
#     win = GraphWin("Calibration Screen", screenx, screeny)
#     win.setBackground("black")
#
#     # Location of the 6 dots. Right now is 2row x 3cols, equally spaced
#     topleft = Point(screenx / 4, screeny / 3)
#     topmid = Point(screenx * 2 / 4, screeny / 3)
#     topright = Point(screenx * 3 / 4, screeny / 3)
#     botleft = Point(screenx / 4, screeny * 2 / 3)
#     botmid = Point(screenx * 2 / 4, screeny * 2 / 3)
#     botright = Point(screenx * 3 / 4, screeny * 2 / 3)
#
#     # points drawn with 'blue' fill
#     ctopleft = Circle(topleft, 10)
#     ctopleft.draw(win)
#     ctopleft.setFill("blue")
#
#     ctopmiddle = Circle(topmid, 10)
#     ctopmiddle.draw(win)
#     ctopmiddle.setFill("blue")
#
#     ctopright = Circle(topright, 10)
#     ctopright.draw(win)
#     ctopright.setFill("blue")
#
#     cbotleft = Circle(botleft, 10)
#     cbotleft.draw(win)
#     cbotleft.setFill("blue")
#
#     cbotmid = Circle(botmid, 10)
#     cbotmid.draw(win)
#     cbotmid.setFill("blue")
#
#     cbotright = Circle(botright, 10)
#     cbotright.draw(win)
#     cbotright.setFill("blue")
#
#     # click will close
#     win.getMouse()
#     win.close()
#
# display_to_screen()
