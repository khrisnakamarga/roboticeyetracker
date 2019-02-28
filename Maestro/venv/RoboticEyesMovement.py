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

import maestro # maestro library
import time # for sleeping
import numpy, scipy.io



def main():
    initialize('COM7') # check device manager!
    accelLim = 100
    velLim = 50
    info = [accelLim, velLim]
    setParam(accelLim, velLim)
    position = []
    t = []

    duration = 4 #duration of the movement

    rotateNeck(4000)
    time.sleep(duration)

    #step input
    servo.setTarget(11, 8000)
    start = time.time()
    while time.time() - start <= duration:
        position.append(servo.getPosition(11))
        t.append(time.time() - start)

    time.sleep(duration)

    scipy.io.savemat('step10.mat', mdict={'pos': position, 't':t, 'info':info})
    servosOff()

# post: initializes the Pololu Controller
def initialize(port):
    global servo
    servo = maestro.Controller('COM7')

# pre: pass in values between 4000 - 6000
# post: nods the head to the final location
# parameter: final = final vertical location
def nod(final):
    rightPillarCh = 1
    leftPillarCh = 2
    servo.setTarget(rightPillarCh,final)
    servo.setTarget(leftPillarCh, final)
    time.sleep(3)

# 6,000 : neutral position (looking front)
# pre: PLEASE HOLD THE ROBOT!!! MIGHT FALL!!!
#      INITIALLY, THE ACCELERATION IS SUPER HIGH!
# post: rotates the neck to the final position specified location
# parameter: final = final neck position
def rotateNeck(final):
    neck = 11
    # servo.setAccel(11, 0) #faster response
    # servo.setSpeed(11, 8) #faster response
    servo.setTarget(neck, final)
    while servo.getPosition(neck) != final:
        time.sleep(0.5)

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
    horEye = 0
    horEyeR = 6
    servo.setTarget(horEye, final)
    time.sleep(0.5)
    servo.setTarget(horEyeR, final)
    time.sleep(2)
    # while servo.getPosition(horEye) != final & \
    #       servo.getPosition(horEyeR) != final:
    #     time.sleep(0.5)

# idk bruh I'm tired it's 3 AM frick
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