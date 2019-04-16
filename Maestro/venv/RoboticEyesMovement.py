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
lHorEye = 0 # Left Eye Horizontal Motion
rPillar = 1 # Right Neck Pillar
lPillar = 2 # Left Neck Pillar
lVertEye = 3 # Left Eye Vertical Motion
rHorEye = 6 # Right Eye Horizontal Motion
rVertEye = 7 # Right Eye Vertical Motion
neck = 11 # Horizontal Neck Motion
neckInitCoord = 4500
rPillarInitCoord = 5000
lPillarInitCoord = 5250
eyeHorInitCoord = 3000
eyeVertInitCoord = 3000
uicount = 1

# vert eye: 2600 - 3120

def main():
    joystickControlV2()

#LIMITS
#neck 9600 2800
#rpillar 5810 4030
#lpillar 5920 4140
#
def joystickControlV2():
    initialize()
    accelLim = 0
    velLim = 0
    setParam(accelLim, velLim)
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord
    global eyeHorInitCoord
    global eyeVertInitCoord
    # for i in range(10):
    #     neckInitCoord += 500
    #     rotateNeck(neckInitCoord)
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
                rotateNeck(neckInitCoord)
            elif keyboard.is_pressed('d'):
                if neckInitCoord < 9600:
                    neckInitCoord += 100
                rotateNeck(neckInitCoord)
            elif keyboard.is_pressed('o'):
                eyeHorInitCoord -= 10
                eyeHor(eyeHorInitCoord)
            elif keyboard.is_pressed('p'):
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
                servosOff()

            # os.system('cls')
            # print("Neck Rotation = " + str(neckInitCoord))
            # print("Right Pillar = " + str(rPillarInitCoord))
            # print("Left Pillar = " + str(lPillarInitCoord))
            global uicount
            uicount += 1
            if uicount == 5:
                uicount = 0
                updateui()
            time.sleep(0.005)
        except KeyboardInterrupt:
            servosOff(eyeHorInitCoord)  # if user pressed a key other than the given key the loop will break

# post: prints the servo coordinates to the console
def updateui():
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
def eyeMove(rx, ry, lx, ly):
    servo.setTarget(lHorEye, lx)
    servo.setTarget(lVertEye, ly)
    servo.setTarget(rHorEye, rx)
    servo.setTarget(rVertEye, ry)

# post: first prototype of the joystick controller
#       uses keypad to command the neck to go to a certain location
def joystickControlV1():
    initialize()
    accelLim = 0
    velLim = 0
    setParam(accelLim, velLim)
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                rotateNeck(4500)
            elif keyboard.is_pressed('w'):
                rotateNeck(5000)
            elif keyboard.is_pressed('e'):
                rotateNeck(5500)
            elif keyboard.is_pressed('r'):
                rotateNeck(6000)
            elif keyboard.is_pressed('i'):
                rotateNeck(6500)
            elif keyboard.is_pressed('o'):
                rotateNeck(7000)
            elif keyboard.is_pressed('p'):
                rotateNeck(7500)
            elif keyboard.is_pressed('['):
                rotateNeck(8000)
        except KeyboardInterrupt:
            servosOff()  # if user pressed a key other than the given key the loop will break

# post: samples the servo coordinate at each time step provided the servo to be moved, movement settings,
#       and the final position of the servo
def stepResponse():
    initialize('COM7') # check device manager!
    servo.setTarget(11, 2410)
    accelLim = 0
    velLim = 20
    info = [accelLim, velLim]
    setParam(accelLim, velLim)
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
    servosOff()

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
def rotateNeck(final):
    servo.setTarget(neck, final)

# pre: input valid channel number (check the hardware connection)
# post: sets the maximum acceleration for all the channels
# parameter:
#   maxAccel = maximum acceleration allowed (0 is inf)
#   maxSpeed = maximum speed allowed (0 is inf)
def setParam(maxAccel, maxSpeed):
    # Specific for 12 channel Pololu board
    for ch in range(12):
        servo.setAccel(ch, maxAccel)
        servo.setSpeed(ch, maxSpeed)

# post: prints and returns the selected servo's position
def getPos(ch):
    location = servo.getPosition(ch)
    print(location)
    return location

# 5000 right 2500 left
# delay between left and right
def eyeHor(final):
    servo.setTarget(lHorEye, final)
    servo.setTarget(rHorEye, final-500)


# def eyeHorBoth(final):


# right eye vert movement does not work
def eyeVert(final):
    servo.setTarget(rVertEye, final)
    servo.setTarget(lVertEye, final)

# turns all the servos off
def servosOff():
    for ch in range(12):
        servo.setTarget(ch, 0)



if __name__ == "__main__":
    main()