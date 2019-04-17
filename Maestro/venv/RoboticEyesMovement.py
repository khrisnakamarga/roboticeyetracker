import maestro  # maestro library
import time  # for sleeping
import numpy
import scipy.io
import keyboard
import os
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

# vert eye: 2600 - 3120

#LIMITS
#neck 9600 2800
#rpillar 5810 4030
#lpillar 5920 4140


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
    # for i in range(10):
    #     neckInitCoord += 500
    #     rotate_neck(neckInitCoord)
    #     time.sleep(1)
    # t1 = threading.Thread(target=textUI)

    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                if rPillarInitCoord > 4030:
                    rPillarInitCoord -= 10
                if lPillarInitCoord < 5920:
                    lPillarInitCoord += 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('e'):
                if rPillarInitCoord < 5810:
                    rPillarInitCoord += 10
                if lPillarInitCoord > 4140:
                    lPillarInitCoord -= 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('w'):
                if rPillarInitCoord < 5810:
                    rPillarInitCoord += 10
                if lPillarInitCoord < 5920:
                    lPillarInitCoord += 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('s'):
                if rPillarInitCoord > 4030:
                    rPillarInitCoord -= 10
                if lPillarInitCoord > 4140:
                    lPillarInitCoord -= 10
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
                eyeHorInitCoord -= 10
                eye_hor(eyeHorInitCoord)
            elif keyboard.is_pressed('p'):
                eyeHorInitCoord += 10
                eye_hor(eyeHorInitCoord)
            elif keyboard.is_pressed('t'):
                if eyeVertInitCoord > 2600:
                    eyeVertInitCoord -= 10
                eye_vert(eyeVertInitCoord)
            elif keyboard.is_pressed('g'):
                if eyeVertInitCoord < 3120:
                    eyeVertInitCoord += 10
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
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord
    global eyeHorInitCoord
    global eyeVertInitCoord

    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('e'):  # if key 'q' is pressed
                if rPillarInitCoord > 4030:
                    rPillarInitCoord -= 10
                if lPillarInitCoord < 5920:
                    lPillarInitCoord += 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('q'):
                if rPillarInitCoord < 5810:
                    rPillarInitCoord += 10
                if lPillarInitCoord > 4140:
                    lPillarInitCoord -= 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('w'):
                if rPillarInitCoord < 5810:
                    rPillarInitCoord += 10
                if lPillarInitCoord < 5920:
                    lPillarInitCoord += 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('s'):
                if rPillarInitCoord > 4030:
                    rPillarInitCoord -= 10
                if lPillarInitCoord > 4140:
                    lPillarInitCoord -= 10
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
                eyeHorInitCoord -= 10
                eyeHor(eyeHorInitCoord)
            elif keyboard.is_pressed('o'):
                eyeHorInitCoord += 10
                eyeHor(eyeHorInitCoord)
            elif keyboard.is_pressed('t'):
                if eyeVertInitCoord > 2600:
                    eyeVertInitCoord -= 10
                eyeVert(eyeVertInitCoord)
            elif keyboard.is_pressed('g'):
                if eyeVertInitCoord < 3120:
                    eyeVertInitCoord += 10
                eyeVert(eyeVertInitCoord)
            elif keyboard.is_pressed('z'):
                servos_off()

            # os.system('cls')
            # print("Neck Rotation = " + str(neckInitCoord))
            # print("Right Pillar = " + str(rPillarInitCoord))
            # print("Left Pillar = " + str(lPillarInitCoord))
            global uicount
            uicount += 1
            if uicount == 5:
                uicount = 0
                update_ui()
            time.sleep(0.005)
        except KeyboardInterrupt:
            servos_off()  # if user pressed a key other than the given key the loop will break


# post: prints the servo coordinates to the console
def update_ui():
    os.system('cls')
    print("Neck Rotation = " + str(neckInitCoord))
    print("Right Pillar = " + str(rPillarInitCoord))
    print("Left Pillar = " + str(lPillarInitCoord))
    print("Eyes = " + str(eyeHorInitCoord))


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
    initialize('COM7') # check device manager!
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
        time.sleep(0.1);
        position.append(servo.getPosition(11))
        t.append(time.time() - start)

    time.sleep(duration)

    scipy.io.savemat('step13.mat', mdict={'pos': position, 't':t, 'info':info})
    servos_off()


# post: initializes the Pololu Controller
def initialize():
    global servo
    servo = maestro.Controller('COM7')
    servo.setTarget(1, 5000)
    servo.setTarget(2, 5250)
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
    servo.setTarget(lHorEye, final)
    servo.setTarget(rHorEye, final-500)


# def eyeHorBoth(final):


# right eye vert movement does not work
def eye_vert(final):
    servo.setTarget(rVertEye, final)
    servo.setTarget(lVertEye, final)


# turns all the servos off
def servos_off():
    for ch in range(12):
        servo.setTarget(ch, 0)


if __name__ == "__main__":
    keyboard_control_front()

