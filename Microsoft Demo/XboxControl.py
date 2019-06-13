import maestro  # maestro library
import time  # for sleeping
import save_servo_state_left as save_left  # saving left eye calibration map
import save_servo_state_right as save_right  # saving right eye calibration map
import coordinate_gen as cg  # generating the grid for the calibration map
import numpy as np
from scipy import interpolate
import load_calib  # to pre-load the calibration map

# GLOBAL VARIABLES
# Pololu Channels
# ANATOMICAL LEFT RIGHT
rPillar = 1  # Right Neck Pillar
lPillar = 2  # Left Neck Pillar
rHorEye = 0  # Left Eye Horizontal Motion
rVertEye = 3  # Left Eye Vertical Motion
lHorEye = 6  # Right Eye Horizontal Motion
lVertEye = 7  # Right Eye Vertical Motion
neck = 11  # Horizontal Neck Motion

# These variables change as the configuration of the robot changes
neckInitCoord = 6000  # faces the front of the test rig
rPillarInitCoord = 4900  # zero head elevation for the right pillar
lPillarInitCoord = 5100  # zero head elevation for the left pillar
eyeHorInitCoord = 3000  # eyes in the middle horizontally
eyeVertInitCoord = 3000  # eyes in the middle vertically


# # Right Eye (anatomical) limits
# class RightEye:
#     def __init__(self, left=3400, right=4000, up=2350, down=3010):
#         self.left = left
#         self.right = right
#         self.up = up
#         self.down = down


# post: initializes the Pololu Controller
def initialize():
    global servo
    servo = maestro.Controller('COM7')  #COM7 on Khrisna's
    servo.setTarget(rPillar, rPillarInitCoord - 280)
    servo.setTarget(lPillar, lPillarInitCoord - 280)
    servo.setTarget(lHorEye, 3715)
    servo.setTarget(lVertEye, 2560)
    time.sleep(1)

# turns all the servos off
def servos_off():
    for ch in range(12):
        servo.setTarget(ch, 0)


# linear relationship
def joystick_for_eye(joystick_x_coordinate):
    return joystick_x_coordinate*(4000 - 3400) + 3715


# linear relationship
def joystick_for_eye_r(joystick_y_coordinate):
    return -joystick_y_coordinate*(3010 - 2350) + 2560


import pygame
pygame.init()


joysticks = []
clock = pygame.time.Clock()

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    print("Detected Joystick '", joysticks[-1].get_name(), "'")

xbox = joysticks[-1]

# global variables
# States
CALIBRATE = True
CONTROL = False
# initial values of servo middle point
x_axis = 3715
y_axis = 2560


def main():
    initialize()

    # GLOBAL VARIABLES
    # Pololu Channels
    # NOT ANATOMICAL LEFT RIGHT
    rPillar = 1  # Right Neck Pillar
    lPillar = 2  # Left Neck Pillar
    rHorEye = 0  # Left Eye Horizontal Motion
    rVertEye = 3  # Left Eye Vertical Motion
    lHorEye = 6  # Right Eye Horizontal Motion
    lVertEye = 7  # Right Eye Vertical Motion
    neck = 11  # Horizontal Neck Motion

    # These variables change as the configuration of the robot changes
    neckInitCoord = 6000  # faces the front of the test rig
    rPillarInitCoord = 4900  # zero head elevation for the right pillar
    lPillarInitCoord = 5100  # zero head elevation for the left pillar
    eyeHorInitCoord = 3000  # eyes in the middle horizontally
    eyeVertInitCoord = 3000  # eyes in the middle vertically

    white = (255, 255, 255)  # RGB
    red = (255, 0, 0)

    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CONTROL")

    pygame.display.update()

    gameExit = False

    while not gameExit:
        # pygame display
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        # if event.type == pygame.JOYBUTTONDOWN:
        #     if event.button == 0:
        #         lead_y = lead_y - 10
        #     if event.button == 2:
        #         lead_y = lead_y + 10
        #     if event.button == 3:
        #         lead_x = lead_x - 10
        #     if event.button == 1:
        #         lead_x = lead_x + 10
        lead_y = xbox.get_axis(1) * 200 + 300
        lead_x = xbox.get_axis(0) * 200 + 300
        gameDisplay.fill(red)

        pygame.draw.rect(gameDisplay, white, [lead_x, lead_y, 20, 20])

        pygame.display.update()

        # pygame display

        # buttons
        increment = 10
        # button press
        if xbox.get_button(3):  # y button
            rPillarInitCoord += increment
            lPillarInitCoord += increment
        if xbox.get_button(0):  # a button
            rPillarInitCoord -= increment
            lPillarInitCoord -= increment
        if xbox.get_button(2):  # x button
            neckInitCoord -= increment  # move neck cw
        if xbox.get_button(1):  # b button
            neckInitCoord += increment  # move neck ccw

        # changing the variables that is used to command the servo
        x_axis = joystick_for_eye(-xbox.get_axis(0))
        y_axis = joystick_for_eye_r(-xbox.get_axis(1))

        # actuate in the test rig
        servo.setTarget(rHorEye, x_axis)
        servo.setTarget(rVertEye, y_axis)
        servo.setTarget(neck, neckInitCoord)
        servo.setTarget(rPillar, rPillarInitCoord)
        servo.setTarget(lPillar, lPillarInitCoord)

    pygame.quit()
    servos_off()


# Calibration algorithm for the right anatomical eye
def joystick_proportional_control_right():
    global x_axis
    global y_axis
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord

    # initialize()  # separate initialize
    white = (255, 255, 255)  # RGB
    red = (255, 0, 0)

    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CONTROL")

    pygame.display.update()

    gameExit = False

    while not gameExit:
        # pygame display
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        lead_y = xbox.get_axis(1)*200 + 300
        lead_x = xbox.get_axis(0)*200 + 300
        gameDisplay.fill(red)

        pygame.draw.rect(gameDisplay, white, [lead_x, lead_y, 20, 20])

        pygame.display.update()

        # pygame display


        #buttons
        x_increment = -xbox.get_axis(0)*10
        y_increment = xbox.get_axis(1)*10
        increment = 20

        # changing the variables that is used to command the servo
        if abs(x_increment) > 1:  # cutoff to avoid drifting
            x_axis += x_increment
        if abs(y_increment) > 1:  # cutoff to avoid drifting
            y_axis += y_increment
        # button press
        if xbox.get_button(3):  # y button
            rPillarInitCoord += increment
            lPillarInitCoord += increment
        if xbox.get_button(0):  # a button
            rPillarInitCoord -= increment
            lPillarInitCoord -= increment
        if xbox.get_button(2):  # x button
            neckInitCoord -= increment  # move neck cw
        if xbox.get_button(1):  # b button
            neckInitCoord += increment  # move neck ccw
        if xbox.get_button(6):  # showing the value of servo command
            print(x_axis)
            print(y_axis)
            time.sleep(0.5)  # debounce
        if xbox.get_button(5):  # rb
            save_right.save_state(x_axis, y_axis)
            cg.increment_index()
            time.sleep(0.25)  # debounce

        if xbox.get_button(9):  # right joystick (for resetting the calibration map
            cg.reset()  # start the coordinate from 0, 0
            save_right.reset_everything()  # emptying the calibration matrix

        if xbox.get_button(7):  # start
            pygame.quit()
            cg.reset()  # resetting the matrix index
            break


        # actuate in the test rig
        servo.setTarget(rHorEye, x_axis)
        servo.setTarget(rVertEye, y_axis)
        servo.setTarget(neck, neckInitCoord)
        servo.setTarget(rPillar, rPillarInitCoord)
        servo.setTarget(lPillar, lPillarInitCoord)

    pygame.quit()


def joystick_proportional_control_together():
    global x_axis
    global y_axis
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord

    # initialize()  # separate initialize
    white = (255, 255, 255)  # RGB
    red = (255, 0, 0)

    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CONTROL")

    pygame.display.update()

    gameExit = False

    while not gameExit:
        # pygame display
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        lead_y = xbox.get_axis(1)*200 + 300
        lead_x = xbox.get_axis(0)*200 + 300
        gameDisplay.fill(red)

        pygame.draw.rect(gameDisplay, white, [lead_x, lead_y, 20, 20])

        pygame.display.update()

        # pygame display


        #buttons
        x_increment = -xbox.get_axis(0)*10
        y_increment = xbox.get_axis(1)*10
        increment = 20

        # changing the variables that is used to command the servo
        if abs(x_increment) > 1:  # cutoff to avoid drifting
            x_axis += x_increment
        if abs(y_increment) > 1:  # cutoff to avoid drifting
            y_axis += y_increment
        # button press
        if xbox.get_button(3):  # y button
            rPillarInitCoord += increment
            lPillarInitCoord += increment
        if xbox.get_button(0):  # a button
            rPillarInitCoord -= increment
            lPillarInitCoord -= increment
        if xbox.get_button(2):  # x button
            neckInitCoord -= increment  # move neck cw
        if xbox.get_button(1):  # b button
            neckInitCoord += increment  # move neck ccw
        if xbox.get_button(6):  # showing the value of servo command
            print(x_axis)
            print(y_axis)
            time.sleep(0.5)  # debounce
        if xbox.get_button(5):  # rb
            save_right.save_state(x_axis, y_axis)
            cg.increment_index()
            time.sleep(0.25)  # debounce

        if xbox.get_button(9):  # right joystick (for resetting the calibration map
            cg.reset()  # start the coordinate from 0, 0
            save_right.reset_everything()  # emptying the calibration matrix

        if xbox.get_button(7):  # start
            pygame.quit()
            cg.reset()  # resetting the matrix index
            break


        # actuate in the test rig
        servo.setTarget(rHorEye, x_axis)
        servo.setTarget(rVertEye, y_axis)
        servo.setTarget(lHorEye,  + 100)
        servo.setTarget(lVertEye, -y_axis)
        servo.setTarget(neck, neckInitCoord)
        servo.setTarget(rPillar, rPillarInitCoord)
        servo.setTarget(lPillar, lPillarInitCoord)

    pygame.quit()
    servos_off()


# Calibration algorithm for the left anatomical eye
def joystick_proportional_control_left():
    global x_axis
    global y_axis
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord

    pygame.init()

    joysticks = []
    clock = pygame.time.Clock()

    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print("Detected Joystick '", joysticks[-1].get_name(), "'")

    xbox = joysticks[-1]

    # initialize()  # separate initialize
    white = (255, 255, 255)  # RGB
    red = (255, 0, 0)

    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CONTROL")

    pygame.display.update()

    gameExit = False

    while not gameExit:
        # pygame display
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        lead_y = xbox.get_axis(1) * 200 + 300
        lead_x = xbox.get_axis(0) * 200 + 300
        gameDisplay.fill(red)

        pygame.draw.rect(gameDisplay, white, [lead_x, lead_y, 20, 20])

        pygame.display.update()

        # pygame display

        x_increment = -xbox.get_axis(0) * 10
        y_increment = -xbox.get_axis(1) * 10
        increment = 20

        # changing the variables that is used to command the servo
        if abs(x_increment) > 1:  # cutoff to avoid drifting
            x_axis += x_increment  # horizontal servo command
        if abs(y_increment) > 1:  # cutoff to avoid drifting
            y_axis += y_increment  # vertical servo command
        # button presses
        if xbox.get_button(3):  # y button
            rPillarInitCoord += increment
            lPillarInitCoord += increment
        if xbox.get_button(0):  # a button
            rPillarInitCoord -= increment
            lPillarInitCoord -= increment
        if xbox.get_button(2):  # x button
            neckInitCoord -= increment  # move neck cw
        if xbox.get_button(1):  # b button
            neckInitCoord += increment  # move neck ccw
        if xbox.get_button(6):  # showing the value of servo command
            print(x_axis)
            print(y_axis)
            time.sleep(0.5)  # debounce
        if xbox.get_button(5):  # rb
            save_left.save_state(x_axis, y_axis)
            cg.increment_index()
            time.sleep(0.25)  # debounce
        if xbox.get_button(9):  # right joystick (for resetting the calibration map
            cg.reset()  # start the coordinate from 0, 0
            save_left.reset_everything()  # emptying the calibration matrix
        if xbox.get_button(7):  # start
            cg.reset()  # resetting the matrix index
            break

        # actuate in the test rig
        servo.setTarget(lHorEye, x_axis)
        servo.setTarget(lVertEye, y_axis)
        servo.setTarget(neck, neckInitCoord)
        servo.setTarget(rPillar, rPillarInitCoord)
        servo.setTarget(lPillar, lPillarInitCoord)

    pygame.quit()
    servos_off()


# stares at the grid points
# if you want to change the grid geometry, please edit cg and save_servo
def grid():
    col = cg.col
    row = cg.row
    x = np.arange(1, col+1, 1)
    y = np.arange(1, row+1, 1)
    # debugging
    # print(x)
    # print(y)

    # left eye calibration map
    X_screen_left = save_left.array_final_x
    Y_screen_left = save_left.array_final_y

    # right eye calibration map
    X_screen_right = save_right.array_final_x
    Y_screen_right = save_right.array_final_y

    sleepytime = 0.3

    # sweeps right, then repeats downwards
    for i in range(row):
        for j in range(col):
            # move right eye
            servo.setTarget(rHorEye, X_screen_right[i][j])
            servo.setTarget(rVertEye, Y_screen_right[i][j])
            # move left eye
            servo.setTarget(lHorEye, X_screen_left[i][j])
            servo.setTarget(lVertEye, Y_screen_left[i][j])

            time.sleep(sleepytime)


# uses the joystick to control gaze location to the screen
# DOES NOT WORK
def joystick_screen():
    x_axis = 1
    y_axis = 1

    pygame.init()

    joysticks = []
    clock = pygame.time.Clock()

    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print("Detected Joystick '", joysticks[-1].get_name(), "'")

    xbox = joysticks[-1]

    # initialize()  # separate initialize
    white = (255, 255, 255)  # RGB
    red = (255, 0, 0)

    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CONTROL")

    pygame.display.update()

    gameExit = False

    while not gameExit:
        # pygame display
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        lead_y = xbox.get_axis(1) * 200 + 300
        lead_x = xbox.get_axis(0) * 200 + 300
        gameDisplay.fill(red)

        pygame.draw.rect(gameDisplay, white, [lead_x, lead_y, 20, 20])

        pygame.display.update()

        # pygame display

        x_increment = xbox.get_axis(0)
        y_increment = xbox.get_axis(1)

        # changing the variables that is used to command the servo
        if abs(x_increment) > 0.2:  # cutoff to avoid drifting
            x_axis += x_increment  # horizontal servo command
        if abs(y_increment) > 0.2:  # cutoff to avoid drifting
            y_axis += y_increment  # vertical servo command
        # button presses
        if xbox.get_button(6):  # showing the value of servo command
            print(x_axis)
            print(y_axis)
            time.sleep(0.25)  # debounce

        # actuate in the test rig
        eyemove_interp_grid(x_axis, y_axis)

    pygame.quit()
    servos_off()


def eyemove_interp_grid(x_grid, y_grid):
    # setting up the coordinate points
    x = np.arange(1, cg.col+1, 1)
    y = np.arange(1, cg.row+1, 1)
    y_grid = cg.row+1 - y_grid
    # debugging
    # print(x)
    # print(y)

    # repopulating the calibration matrix

    # left eye calibration map
    X_screen_left = save_left.array_final_x
    Y_screen_left = save_left.array_final_y

    # right eye calibration map
    X_screen_right = save_right.array_final_x
    Y_screen_right = save_right.array_final_y

    # interpolation model
    f_X_screen_left = interpolate.interp2d(x, y, X_screen_left, kind='linear')
    f_Y_screen_left = interpolate.interp2d(x, y, Y_screen_left, kind='linear')
    f_X_screen_right = interpolate.interp2d(x, y, X_screen_right, kind='linear')
    f_Y_screen_right = interpolate.interp2d(x, y, Y_screen_right, kind='linear')

    # print(int(f_X_screen(x_grid, y_grid)))
    # print(int(f_Y_screen(x_grid, y_grid)))
    servo.setTarget(lHorEye, int(f_X_screen_left(x_grid, y_grid)))
    servo.setTarget(lVertEye, int(f_Y_screen_left(x_grid, y_grid)))
    servo.setTarget(rHorEye, int(f_X_screen_right(x_grid, y_grid)))
    servo.setTarget(rVertEye, int(f_Y_screen_right(x_grid, y_grid)))

    sleepytime = 0.3
    # time.sleep(sleepytime)


def joystick_eyes_together():
    global x_axis
    global y_axis
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord

    pygame.init()

    joysticks = []
    clock = pygame.time.Clock()

    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print("Detected Joystick '", joysticks[-1].get_name(), "'")

    xbox = joysticks[-1]

    # initialize()  # separate initialize
    white = (255, 255, 255)  # RGB
    red = (255, 0, 0)

    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CONTROL")

    pygame.display.update()

    gameExit = False

    # initial values of servo middle point
    x_axis_right = 3715
    y_axis_right = 2560
    x_axis_left = 3715
    y_axis_left = 2560

    while not gameExit:
        # pygame display
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        lead_y = xbox.get_axis(1) * 200 + 300
        lead_x = xbox.get_axis(0) * 200 + 300
        gameDisplay.fill(red)

        pygame.draw.rect(gameDisplay, white, [lead_x, lead_y, 20, 20])

        pygame.display.update()

        # pygame display

        x_increment_right = -xbox.get_axis(0) * 10
        y_increment_right = xbox.get_axis(1) * 10
        x_increment_left = -xbox.get_axis(4) * 10
        y_increment_left = -xbox.get_axis(3) * 10
        increment = 20

        # changing the variables that is used to command the servo
        if abs(x_increment_right) > 1:  # cutoff to avoid drifting
            x_axis_right += x_increment_right  # horizontal servo command
        if abs(y_increment_right) > 1:  # cutoff to avoid drifting
            y_axis_right += y_increment_right  # vertical servo command
        # changing the variables that is used to command the servo
        if abs(x_increment_left) > 1:  # cutoff to avoid drifting
            x_axis_left += x_increment_left  # horizontal servo command
        if abs(y_increment_right) > 1:  # cutoff to avoid drifting
            y_axis_left += y_increment_left  # vertical servo command
        # button presses
        if xbox.get_button(3):  # y button
            rPillarInitCoord += increment
            lPillarInitCoord += increment
        if xbox.get_button(0):  # a button
            rPillarInitCoord -= increment
            lPillarInitCoord -= increment
        if xbox.get_button(2):  # x button
            neckInitCoord -= increment  # move neck cw
        if xbox.get_button(1):  # b button
            neckInitCoord += increment  # move neck ccw

        # actuate in the test rig
        if (abs(x_increment_left) > 2) | (abs(y_increment_left) > 2):
            servo.setTarget(lHorEye, x_axis_left)
            servo.setTarget(lVertEye, y_axis_left)
            servo.setTarget(rHorEye, x_axis_right)
            servo.setTarget(rVertEye, y_axis_right)
        elif (abs(x_increment_right) > 2) | (abs(y_increment_right) > 2):
            servo.setTarget(lHorEye, x_axis_left)
            servo.setTarget(lVertEye, y_axis_left)
        servo.setTarget(neck, neckInitCoord)
        servo.setTarget(rPillar, rPillarInitCoord)
        servo.setTarget(lPillar, lPillarInitCoord)

    pygame.quit()
    servos_off()


class Shapes(object):
    # draws a rectangle with x and y as starting points and l1 and l2 as the sides
    @staticmethod
    def rectangle(x, y, l1, l2):
        sleepytime = 1
        eyemove_interp_grid(x, y)
        time.sleep(sleepytime)

        eyemove_interp_grid(x + l1, y)
        time.sleep(sleepytime)

        eyemove_interp_grid(x + l1, y + l2)
        time.sleep(sleepytime)

        eyemove_interp_grid(x, y + l2)
        time.sleep(sleepytime)

        eyemove_interp_grid(x, y)
        time.sleep(sleepytime)

    @staticmethod
    # draw a square with sides = side
    def square(x, y, side):
        Shapes.rectangle(x, y, side, side)

    @staticmethod
    # draw a triangle
    def circle(x, y, radius, rotations):
        theta = np.arange(0, rotations*2*np.pi, 0.1)
        # print(theta)
        for i in theta:
            eyemove_interp_grid(x + radius*np.cos(i), y + radius*np.sin(i))
            time.sleep(0.001)


# pre: input valid channel number (check the hardware connection)
# post: sets the maximum acceleration for all the channels
# parameter:
#   maxAccel = maximum acceleration allowed (0 is inf)
#   maxSpeed = maximum speed allowed (0 is inf)
def set_param(maxAccel, maxSpeed):
    # Specific for 12 channel Pololu board
    for ch in range(12):
        servo.setAccel(ch, maxAccel)
        servo.setSpeed(ch, maxSpeed)


if __name__ == '__main__':
    initialize()
    # main()

    # working demo
    load_prev = input("Would you like to pre-load the calibration map? (y/n)")
    if load_prev == "n":
        joystick_proportional_control_right()
        joystick_proportional_control_left()
    else:
        left_eye_calibration = load_calib.CalibrationMap(3, 3)
        left_eye_calibration.load('left_x.csv', 'left_y.csv')
        right_eye_calibration = load_calib.CalibrationMap(3, 3)
        right_eye_calibration.load('right_x.csv', 'right_y.csv')

        # left eye calibration map
        save_left.array_final_x = left_eye_calibration.x_map
        save_left.array_final_y = left_eye_calibration.y_map

        # right eye calibration map
        save_right.array_final_x = right_eye_calibration.x_map
        save_right.array_final_y = right_eye_calibration.y_map

    set_param(10, 0)  # limitting speed
    # grid()
    # set_param(0, 0)  # limitting speed
    # Shapes.circle(3, 3, 1, 10)
    # set_param(10, 10)  # limitting speed
    # Shapes.square(3, 1, 1)
    print(save_left.array_final_x)

    # #telling calib that everything is fine
    # servo.setTarget(rPillar, rPillarInitCoord - 100)
    # servo.setTarget(lPillar, lPillarInitCoord - 100)
    # time.sleep(5)
    # servo.setTarget(rPillar, rPillarInitCoord - 280)
    # servo.setTarget(lPillar, lPillarInitCoord - 280)
    # time.sleep(1)

    # Calibration
    eyemove_interp_grid(1.8, 2.1)  # middle
    print("next")
    time.sleep(5)
    eyemove_interp_grid(2, 3)  # top
    print("next")
    time.sleep(5)
    eyemove_interp_grid(1, 1)  # left
    print("next")
    time.sleep(5)
    eyemove_interp_grid(3, 1)  # right
    print("next")
    time.sleep(5)
    eyemove_interp_grid(1.8, 2.1)  # right
    print("finish")
    time.sleep(5)

    # # drawing shapes
    # set_param(0, 0)
    # Shapes.square(1, 1, 0.5)
    # time.sleep(5)
    # Shapes.square(2, 1, 0.5)
    # time.sleep(5)
    # Shapes.square(2, 2, 0.5)
    # time.sleep(5)
    # Shapes.square(1, 2, 0.5)
    # time.sleep(5)
    # Shapes.square(1.5, 1.5, 1)
    # time.sleep(5)
    # Shapes.square(1.5, 1.5, 1.5)
    # time.sleep(5)
    # eyemove_interp_grid(1.8, 2.1)  # right
    # print("finish")
    # time.sleep(5)



