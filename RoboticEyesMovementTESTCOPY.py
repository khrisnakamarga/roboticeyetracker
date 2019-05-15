import maestro  # maestro library
import time  # for sleeping
import numpy as np
import scipy.io
from scipy import interpolate
import keyboard
import os
import save_servo_state_single_script as save_servo
import coordinate_gen
import threading



'''
Author: Khrisna Kamarga
Project: Microsoft Robotic Eyes Servo Control Script
Description: This script defines head movements and serves as a client of maestro.py
             It defines head and eye movements in terms of common terms and the user
             is able to instruct the servos by accessing the movements defined
To Do:
1. Add method that implements servo limitations
2. Make a class for the channels
3. Give acceleration/velocity limits to the UI
4. Make a script that installs all the libraries

Ideas
1. Convert arbitrary servo positions into angles or something understandable
2. Have predefined script movements stored in Maestro
3. Convert to C++
4. Start small by calibrating gaze location without eye focus

'''

# setting a very high value
# find out the effective pulses


# GLOBAL VARIABLES
# Pololu Channels
# NOT ANATOMICAL LEFT RIGHT
lHorEye = 0  # Left Eye Horizontal Motion
rPillar = 1  # Right Neck Pillar
lPillar = 2  # Left Neck Pillar
lVertEye = 3  # Left Eye Vertical Motion
rHorEye = 6  # Right Eye Horizontal Motion
rVertEye = 7  # Right Eye Vertical Motion
neck = 11  # Horizontal Neck Motion
neckInitCoord = 4500  # faces the front of the test rig
rPillarInitCoord = 5000  # zero head elevation for the right pillar
lPillarInitCoord = 5250  # zero head elevation for the left pillar
eyeHorInitCoord = 3000  # eyes in the middle horizontally
eyeVertInitCoord = 3000  # eyes in the middle vertically
uicount = 1  # counter that updates the console UI


# LIMITS
# neck 9600 2800
# right pillar 5810 4030
# left pillar 5920 4140
# vertical eye: 2600 - 3120

# second version of the joystick controller
# uses the qwe, asd to control the neck and head gaze movement
# uses the op, tg to control the eye movements
# updates the servo coordinates to the UI in the console
def keyboard_control_front():
    initialize()
    accelLim = 0
    velLim = 0
    set_param(accelLim, velLim)
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord
    global eyeHorInitCoord
    global eyeVertInitCoord

    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            resolution = 4
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                if rPillarInitCoord > 4030:
                    rPillarInitCoord -= resolution
                if lPillarInitCoord < 5920:
                    lPillarInitCoord += resolution
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('e'):
                if rPillarInitCoord < 5810:
                    rPillarInitCoord += resolution
                if lPillarInitCoord > 4140:
                    lPillarInitCoord -= resolution
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('w'):
                if rPillarInitCoord < 5810:
                    rPillarInitCoord += resolution
                if lPillarInitCoord < 5920:
                    lPillarInitCoord += resolution
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('s'):
                if rPillarInitCoord > 4030:
                    rPillarInitCoord -= resolution
                if lPillarInitCoord > 4140:
                    lPillarInitCoord -= resolution
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('a'):
                if neckInitCoord > 2800:
                    neckInitCoord -= 100
                rotate_neck(neckInitCoord)
            elif keyboard.is_pressed('d'):
                if neckInitCoord < 9600:
                    neckInitCoord += 100
                rotate_neck(neckInitCoord)
            elif keyboard.is_pressed('o'):
                eyeHorInitCoord -= resolution
                eye_hor(eyeHorInitCoord)
            elif keyboard.is_pressed('p'):
                eyeHorInitCoord += resolution
                eye_hor(eyeHorInitCoord)
            elif keyboard.is_pressed('t'):
                # if eyeVertInitCoord > 2600:
                eyeVertInitCoord -= resolution
                eye_vert(eyeVertInitCoord)
            elif keyboard.is_pressed('g'):
                # if eyeVertInitCoord < 3120:
                eyeVertInitCoord += resolution
                eye_vert(eyeVertInitCoord)
            elif keyboard.is_pressed('z'):
                servos_off()
            # else:
            #     servos_off()

            global uicount
            uicount += 1
            if uicount == 5:
                uicount = 0
                update_ui()
            time.sleep(0.05)
        except KeyboardInterrupt:
            servos_off()  # if user pressed a key other than the given key the loop will break
            exit()


# mirrored
def keyboard_control_back():
    initialize()
    accelLim = 0
    velLim = 0
    set_param(accelLim, velLim)
    resolution = 2

    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord
    global eyeHorInitCoord
    global eyeVertInitCoord

    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('e'):  # if key 'q' is pressed
                if rPillarInitCoord > 4030:
                    rPillarInitCoord -= resolution
                if lPillarInitCoord < 5920:
                    lPillarInitCoord += resolution
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('q'):
                if rPillarInitCoord < 5810:
                    rPillarInitCoord += resolution
                if lPillarInitCoord > 4140:
                    lPillarInitCoord -= resolution
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('w'):
                if rPillarInitCoord < 5810:
                    rPillarInitCoord += resolution
                if lPillarInitCoord < 5920:
                    lPillarInitCoord += resolution
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('s'):
                if rPillarInitCoord > 4030:
                    rPillarInitCoord -= resolution
                if lPillarInitCoord > 4140:
                    lPillarInitCoord -= resolution
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('d'):
                if neckInitCoord > 2800:
                    neckInitCoord -= 100
                rotate_neck(neckInitCoord)
            elif keyboard.is_pressed('a'):
                if neckInitCoord < 9600:
                    neckInitCoord += 100
                rotate_neck(neckInitCoord)
            elif keyboard.is_pressed('p'):
                eyeHorInitCoord -= resolution
                eye_hor(eyeHorInitCoord)
            elif keyboard.is_pressed('o'):
                eyeHorInitCoord += resolution
                eye_hor(eyeHorInitCoord)
            elif keyboard.is_pressed('t'):
                if eyeVertInitCoord > 1600:
                    eyeVertInitCoord -= resolution
                eye_vert(eyeVertInitCoord)
            elif keyboard.is_pressed('g'):
                if eyeVertInitCoord < 3120:
                    eyeVertInitCoord += resolution
                eye_vert(eyeVertInitCoord)
            elif keyboard.is_pressed('z'):


                save_servo.save_state(eyeHorInitCoord,eyeVertInitCoord)
                coordinate_gen.increment_index()

                time.sleep(0.25)

            # os.system('cls')
            # print("Neck Rotation = " + str(neckInitCoord))
            # print("Right Pillar = " + str(rPillarInitCoord))
            # print("Left Pillar = " + str(lPillarInitCoord))
            global uicount
            uicount += 1
            if uicount == 5:
                uicount = 0
                #update_ui()
            time.sleep(0.02)

        except KeyboardInterrupt:
            servos_off()  # if user pressed a key other than the given key the loop will break

        if keyboard.is_pressed('m'):
            break

# post: prints the servo coordinates to the console
def update_ui():
    os.system('cls')
    # print("Neck Rotation = " + str(neckInitCoord))
    # print("Right Pillar = " + str(rPillarInitCoord))
    # print("Left Pillar = " + str(lPillarInitCoord))
    print("Hor Eyes = " + str(eyeHorInitCoord))
    print("Vert Eyes = " + str(eyeVertInitCoord))
    print("Neck = " + str(neckInitCoord))


# post: moves each eye into a point specified by the coordinated
# parameter:
#   rx = right eye's horizontal position
#   ry = right eye's vertical position
#   lx = left eye's horizontal position
#   ly = left eye's vertical position

def eye_move(rx, ry, lx, ly):
    servo.setTarget(lHorEye, lx)
    servo.setTarget(lVertEye, ly)
    servo.setTarget(rHorEye, rx)
    servo.setTarget(rVertEye, ry)




# post: first prototype of the joystick controller
#       uses keypad to command the neck to go to a certain location
def keyboard_control_v1():
    initialize()
    accelLim = 0
    velLim = 0
    set_param(accelLim, velLim)
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                rotate_neck(4500)
            elif keyboard.is_pressed('w'):
                rotate_neck(5000)
            elif keyboard.is_pressed('e'):
                rotate_neck(5500)
            elif keyboard.is_pressed('r'):
                rotate_neck(6000)
            elif keyboard.is_pressed('i'):
                rotate_neck(6500)
            elif keyboard.is_pressed('o'):
                rotate_neck(7000)
            elif keyboard.is_pressed('p'):
                rotate_neck(7500)
            elif keyboard.is_pressed('['):
                rotate_neck(8000)
        except KeyboardInterrupt:
            servos_off()  # if user pressed a key other than the given key the loop will break


# post: samples the servo coordinate at each time step provided the servo to be moved, movement settings,
#       and the final position of the servo
def step_response():
    servo.setTarget(11, 2410)
    accelLim = 0
    velLim = 20
    info = [accelLim, velLim]
    set_param(accelLim, velLim)
    position = []
    t = []

    duration = 4 #duration of the movement

    time.sleep(4)

    #step input
    servo.setTarget(11, 9600)
    start = time.time()
    while time.time() - start <= duration:
        time.sleep(0.1)
        position.append(servo.getPosition(11))
        t.append(time.time() - start)

    time.sleep(duration)

    scipy.io.savemat('step13.mat', mdict={'pos': position, 't':t, 'info':info})
    servos_off()


# post: initializes the Pololu Controller
def initialize():
    global servo
    servo = maestro.Controller('COM5')  #COM7 on Khrisna's
    servo.setTarget(1, 4900)
    servo.setTarget(2, 5100)
    time.sleep(1)
    # servo.setTarget(11, 2000)


# pre: pass in values between 4000 - 6000
# post: nods the head to the final location
# parameter: final = final vertical location
def nod(final):
    servo.setTarget(rPillar,final)
    servo.setTarget(lPillar, final)
    time.sleep(3)


# range : 2,410 - 9600
# 6,000 : neutral position (looking front)
# pre: PLEASE HOLD THE ROBOT!!! MIGHT FALL!!!
#      INITIALLY, THE ACCELERATION IS SUPER HIGH!
# post: rotates the neck to the final position specified location
# parameter: final = final neck position
def rotate_neck(final):
    servo.setTarget(neck, final)


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


# post: prints and returns the selected servo's position
def get_pos(ch):
    location = servo.getPosition(ch)
    print(location)
    return location


# 5000 right 2500 left
# delay between left and right
def eye_hor(final):
    # move_wait(lHorEye, final)
    # move_wait(rHorEye, final-500)
    servo.setTarget(lHorEye, final)
    servo.setTarget(rHorEye, final)


# def eyeHorBoth(final):


# right eye vert movement does not work
def eye_vert(final):
    servo.setTarget(rVertEye, final)
    servo.setTarget(lVertEye, final)


# turns all the servos off
def servos_off():
    for ch in range(12):
        servo.setTarget(ch, 0)


def test():
    # initialize()
    accelLim = 0
    velLim = 0
    set_param(accelLim, velLim)
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord
    global eyeHorInitCoord
    global eyeVertInitCoord
    eye_vert(eyeVertInitCoord)
    rotate_neck(neckInitCoord+1500)
    time.sleep(1)
    # eyeVertInitCoord -= 12
    for vertical in range(5):
        eyeVertInitCoord -= 30
        eye_vert(eyeVertInitCoord)
        for horizontal in range(16):
            eyeHorInitCoord += 30
            eye_hor(eyeHorInitCoord)
            time.sleep(0.2) #ajust for the speed of laser movement

            get_pos(rVertEye)
            print(eyeVertInitCoord - 500)
            print()
            get_pos(rHorEye)
            print(eyeHorInitCoord - 500)
            print()
        eyeHorInitCoord = 2700


# too close to the edge
# eyeHorInitCoord = 2500
# eyeVertInitCoord = 2890  # eyes in the middle vertically
eyeHorInitCoord = 3100
eyeVertInitCoord = 2630


# converts x screen coordinate to servo coordinate
def x_map(x_screen):
    return 3180 - (x_screen * 30)


# converts y screen coordinate to servo coordinate
def y_map(y_screen):
    return 2770 - (y_screen * 30)


def moveEye(x_screen, y_screen):
    eye_hor(x_map(x_screen))
    eye_vert(y_map(y_screen))
    time.sleep(5)

def move_eye_together(x_screen, y_screen):
    err_tresh = 5
    x_step = x_map(x_screen)
    y_step = y_map(y_screen)
    x_error = servo.getPosition(rHorEye) - x_step
    y_error = servo.getPosition(rVertEye) - y_step
    while (abs(x_error) > err_tresh) & (abs(y_error) > err_tresh):
        x_temp = servo.getPosition(rHorEye)
        y_temp = servo.getPosition(rVertEye)
        if x_error < 0:
            eye_hor(servo.getPosition(rHorEye) + 2)
        else:
            eye_hor(servo.getPosition(rHorEye) - 2)
        if y_error < 0:
            eye_vert(servo.getPosition(rVertEye) + 2)
        else:
            eye_vert(servo.getPosition(rVertEye) - 2)
        time.sleep(0.01)
        x_step = x_map(x_screen)
        y_step = y_map(y_screen)
        x_error = servo.getPosition(rHorEye) - x_step
        y_error = servo.getPosition(rVertEye) - y_step


# lesson learned: get pos actually gives u the servo coordinate
# replace global coordinates with gets
def understandingGetPos():
    get_pos(neck)
    servo.setTarget(neck, 3000)
    get_pos(neck)
    servo.setTarget(neck, 6000)
    get_pos(neck)
    time.sleep(1)


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
        rectangle(x, y, side, side)

    @staticmethod
    # draw a triangle
    def circle(x, y, radius, rotations):
        theta = np.arange(0, rotations*2*np.pi, 0.1)
        print(theta)
        for i in theta:
            eyemove_interp_grid(x + radius*np.cos(i), y + radius*np.sin(i))
            time.sleep(0.001)




def trajectory():
    initialize()
    accelLim = 3
    velLim = 3
    set_param(accelLim, velLim)
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord
    global eyeHorInitCoord
    global eyeVertInitCoord
    # eyeVertInitCoord += 50
    # eye_vert(eyeVertInitCoord)
    rotate_neck(neckInitCoord + 1500)
    eye_hor(x_map(0))
    eye_vert(y_map(0))
    time.sleep(1)

    sleepytime = 1

    # eye_hor(x_map(3))
    # eye_vert(y_map(2))
    # time.sleep(sleepytime)
    #
    # eye_hor(x_map(5))
    # eye_vert(y_map(2))
    # time.sleep(sleepytime)
    #
    # eye_hor(x_map(5))
    # eye_vert(y_map(4))
    # time.sleep(sleepytime)
    #
    # eye_hor(x_map(3))
    # eye_vert(y_map(4))
    # time.sleep(sleepytime)
    #
    # eye_hor(x_map(3))
    # eye_vert(y_map(2))
    # time.sleep(sleepytime)

    eye_hor(x_map(1))
    eye_vert(y_map(1))
    time.sleep(sleepytime)

    eye_hor(x_map(2))
    eye_vert(y_map(1))
    time.sleep(sleepytime)

    eye_hor(x_map(2))
    eye_vert(y_map(2))
    time.sleep(sleepytime)

    eye_hor(x_map(1))
    eye_vert(y_map(2))
    time.sleep(sleepytime)

    # eye_hor(x_map(0))
    # eye_vert(y_map(0))
    # time.sleep(1)

    eye_hor(x_map(1))
    eye_vert(y_map(1))
    time.sleep(sleepytime)



    # eye_hor(x_map(13))
    # eye_vert(y_map(0))
    # time.sleep(4)

    # moveEye(1, 1)
    # moveEye(2, 1)
    # moveEye(2, 2)
    # moveEye(1, 1)
    # moveEye(1, 1)


def stare_to_point(x, y):
    sleepytime = 1
    eye_hor(x)
    eye_vert(y)
    time.sleep(sleepytime)


def move_wait(channel, final):
    servo.setTarget(channel, final)
    while True:
        if servo.getPosition(channel) == final:
            break


def grid():

    col = coordinate_gen.col
    row = coordinate_gen.row
    x = np.arange(1, col+1, 1)
    y = np.arange(1, row+1, 1)
    # debugging
    # print(x)
    # print(y)
    xx, yy = np.meshgrid(x, y)
    X_screen = save_servo.left_array_final_x

    Y_screen = save_servo.left_array_final_y

    sleepytime = 0.3

    # sweeps right, then repeats downwards
    for i in range(row):
        for j in range(col):
            eye_hor(X_screen[i][j])
            eye_vert(Y_screen[i][j])
            time.sleep(sleepytime)

    # sweeps left, then repeats upwards
    for i in range(row):
        for j in range(col):
            eye_hor(X_screen[row-1-i][col-1-j])
            eye_vert(Y_screen[row-1-i][col-1-j])
            time.sleep(sleepytime)

    # sweeps down, then repeats right
    for j in range(col):
        for i in range(row):
            eye_hor(X_screen[i][j])
            eye_vert(Y_screen[i][j])
            time.sleep(sleepytime)

    # sweeps up, then repeats left
    for j in range(col):
        for i in range(row):
            eye_hor(X_screen[row-1-i][col-1-j])
            eye_vert(Y_screen[row-1-i][col-1-j])
            time.sleep(sleepytime)


def eyemove_interp_grid(x_grid, y_grid):
    x = np.arange(1, 11, 1)
    y = np.arange(1, 5, 1)
    y_grid = 5 - y_grid
    # debugging
    # print(x)
    # print(y)
    X_screen = [[3840, 3795, 3740, 3685, 3625, 3555, 3490, 3430, 3370, 3315],
                [3865, 3800, 3740, 3685, 3625, 3540, 3480, 3415, 3360, 3300],
                [3855, 3795, 3745, 3690, 3610, 3550, 3485, 3425, 3365, 3315],
                [3855, 3795, 3745, 3670, 3610, 3545, 3480, 3420, 3365, 3305]]
    Y_screen = [[2800, 2800, 2800, 2805, 2805, 2805, 2800, 2800, 2805, 2800],
                [2860, 2865, 2870, 2870, 2870, 2870, 2865, 2865, 2865, 2865],
                [2935, 2935, 2935, 2935, 2930, 2930, 2930, 2930, 2930, 2930],
                [2995, 3005, 3005, 3000, 3000, 3000, 3000, 3000, 3010, 3010]]
    f_X_screen = interpolate.interp2d(x, y, X_screen, kind='cubic')
    f_Y_screen = interpolate.interp2d(x, y, Y_screen, kind='cubic')


    # print(int(f_X_screen(x_grid, y_grid)))
    # print(int(f_Y_screen(x_grid, y_grid)))
    eye_hor(int(f_X_screen(x_grid, y_grid)))
    eye_vert(int(f_Y_screen(x_grid, y_grid)))
    sleepytime = 0.3
    # time.sleep(sleepytime)



def main():
    initialize()
    #test()
    #servos_off()

if __name__ == "__main__":
    #initialize()
    # Shapes.circle(1, 1, 3)
    # stare_to_point(6, 6)
    keyboard_control_back()
    while True:
        grid()
        if keyboard.is_pressed('m'):
            break
    # servos_off()
    # initialize()
    set_param(0, 0)
    servos_off()
    # rotate_neck(6000)
    # time.sleep(1)
    # grid()
    # grid()
    # eyemove_interp_grid(4.5, 2.5)
    # Shapes.rectangle(2, 2, 1, 1)
    # Shapes.circle(3, 2, 1, 100)
    # servos_off()

# new limit: 2870

