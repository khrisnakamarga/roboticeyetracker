import maestro  # maestro library
import time  # for sleeping
import numpy
import scipy.io
import keyboard
import os


'''
Author: Khrisna Kamarga
Project: Microsoft Robotic Eyes Servo Control Script
Description: This script defines head movements and serves as a client of maestro.py
             It defines head and eye movements in terms of common terms and the user
             is able to instruct the servos by accessing the movements defined
To Do:
1. Implement a function that waits until target is achieved (through a list)
2. Add more movements
3. Define limits
4. isMoving()!!!

Ideas
1. Convert arbitrary servo positions into angles or something understandable
2. Have predefined script movements stored in Maestro
3. Convert to C++
4. Start small by calibrating gaze location without eye focus

'''

'''
    # servo.setTarget(1, 5000)
    # servo.setTarget(2, 5000)
    # time.sleep(4)
    # # rotateNeck(6000)
    # # rotateNeck(8000)
    # # rotateNeck(4000)
    # # rotateNeck(6000)
    # # nod(4000)
    # # nod(4000)
    servo.setTarget(1, 5000)
    servo.setTarget(2, 5000)
    time.sleep(4)
    # getPos(0)
    # # nod(4500)
    # eyeHor(4000)
    # eyeHor(2000)
    # eyeHor(4000)
    # eyeHor(2000)
    # getPos(6)
    # eyeHor(3000)
    # getPos(6)
    # for i in range(6):
    #     rotateNeck(4000)
    #     rotateNeck(8000)
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

def main():
    joystickControlV2()

def joystickControlV2():
    initialize()
    accelLim = 50
    velLim = 0
    setParam(accelLim, velLim)
    global neckInitCoord
    global rPillarInitCoord
    global lPillarInitCoord
    global eyeHorInitCoord
    # for i in range(10):
    #     neckInitCoord += 500
    #     rotateNeck(neckInitCoord)
    #     time.sleep(1)

    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                rPillarInitCoord -= 10
                lPillarInitCoord += 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('e'):
                rPillarInitCoord += 10
                lPillarInitCoord -= 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('w'):
                rPillarInitCoord += 10
                lPillarInitCoord += 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('s'):
                rPillarInitCoord -= 10
                lPillarInitCoord -= 10
                servo.setTarget(1, rPillarInitCoord)
                servo.setTarget(2, lPillarInitCoord)
            elif keyboard.is_pressed('a'):
                neckInitCoord -= 100
                rotateNeck(neckInitCoord)
            elif keyboard.is_pressed('d'):
                neckInitCoord += 100
                rotateNeck(neckInitCoord)
            elif keyboard.is_pressed('o'):
                eyeHorInitCoord -= 1000
                eyeHor(eyeHorInitCoord)
            elif keyboard.is_pressed('p'):
                eyeHorInitCoord += 1
                eyeHor(eyeHorInitCoord)
            os.system('cls')
            print("Neck Rotation = " + str(neckInitCoord))
            print("Right Pillar = " + str(rPillarInitCoord))
            print("Left Pillar = " + str(lPillarInitCoord))
            time.sleep(0.01)
        except KeyboardInterrupt:
            servosOff()  # if user pressed a key other than the given key the loop will break

def eyeMove(rx, ry, lx, ly):
    servo.setTarget(lHorEye, lx)
    servo.setTarget(lVertEye, ly)
    servo.setTarget(rHorEye, rx)
    servo.setTarget(rVertEye, ry)


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
    # servo.setAccel(neck, 1) #faster response
    # servo.setSpeed(neck, 1) #faster response
    servo.setTarget(neck, final)
    # while servo.getPosition(neck) != final:
    #     time.sleep(0.5)

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
    time.sleep(0.5)
    servo.setTarget(rHorEye, final)
    time.sleep(2)
    # while servo.getPosition(horEye) != final & \
    #       servo.getPosition(horEyeR) != final:
    #     time.sleep(0.5)

# right eye vert movement does not work
# def eyeVert(final):
#     verEye = 3
#     verEyeR = 7
#     servo.setTarget(horEye, final)
#     while servo.getPosition(verEye) != final & \
#           servo.getPosition(verEyeR) != final:
#           time.sleep(0.5)


def servosOff():
    allChannels = 12
    for ch in range(12):
        servo.setTarget(ch, 0)



if __name__ == "__main__":
    main()