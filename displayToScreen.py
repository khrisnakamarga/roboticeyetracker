from graphics import *

# creates a 1366 x 768 black window (EASY TO CHANGE) and
# draws a 3 x 2 grid of blue dots equally spaced.
# clicking the screen will close program.
def main():
    # background size and color
    # 16:9 aspect ratio window size
    screenx = 1366
    screeny = 768
    win = GraphWin("Calibration Screen", screenx, screeny)
    win.setBackground("black")

    # Location of the 6 dots. Right now is 2row x 3cols, equally spaced
    topleft = Point(screenx / 4, screeny / 3)
    topmid = Point(screenx * 2 / 4, screeny / 3)
    topright = Point(screenx * 3 / 4, screeny / 3)
    botleft = Point(screenx / 4, screeny * 2 / 3)
    botmid = Point(screenx * 2 / 4, screeny * 2 / 3)
    botright = Point(screenx * 3 / 4, screeny * 2 / 3)

    # points drawn with 'blue' fill
    ctopleft = Circle(topleft, 10)
    ctopleft.draw(win)
    ctopleft.setFill("blue")

    ctopmiddle = Circle(topmid, 10)
    ctopmiddle.draw(win)
    ctopmiddle.setFill("blue")

    ctopright = Circle(topright, 10)
    ctopright.draw(win)
    ctopright.setFill("blue")

    cbotleft = Circle(botleft, 10)
    cbotleft.draw(win)
    cbotleft.setFill("blue")

    cbotmid = Circle(botmid, 10)
    cbotmid.draw(win)
    cbotmid.setFill("blue")

    cbotright = Circle(botright, 10)
    cbotright.draw(win)
    cbotright.setFill("blue")

    # click will close
    win.getMouse()
    win.close()

main()