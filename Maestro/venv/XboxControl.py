import maestro  # maestro library
import time  # for sleeping

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

# These variables change as the configuration of the robot changes
neckInitCoord = 6000  # faces the front of the test rig
rPillarInitCoord = 4900  # zero head elevation for the right pillar
lPillarInitCoord = 5100  # zero head elevation for the left pillar
eyeHorInitCoord = 3000  # eyes in the middle horizontally
eyeVertInitCoord = 3000  # eyes in the middle vertically


# Right Eye (anatomical) limits
class RightEye:
    def __init__(self, left=3400, right=4000, up=2350, down=3010):
        self.left = left
        self.right = right
        self.up = up
        self.down = down


# post: initializes the Pololu Controller
def initialize():
    global servo
    servo = maestro.Controller('COM7')  #COM7 on Khrisna's
    servo.setTarget(rPillar, rPillarInitCoord)
    servo.setTarget(lPillar, lPillarInitCoord)
    servo.setTarget(lHorEye, 3715)
    servo.setTarget(lVertEye, 2560)
    time.sleep(1)


def joystick_for_eye(joystick_x_coordinate):
    return joystick_x_coordinate*(4000 - 3400) + 3715


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

if __name__ == '__main__':
    initialize()
    white = (255, 255, 255)  # RGB
    red = (255, 0, 0)

    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CONTROL")

    pygame.display.update()

    gameExit = False


    while not gameExit:
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
        lead_y = xbox.get_axis(1)*200 + 300
        lead_x = xbox.get_axis(0)*200 + 300
        gameDisplay.fill(red)

        pygame.draw.rect(gameDisplay, white, [lead_x, lead_y, 20, 20])

        pygame.display.update()

        hold = False
        #buttons
        increment = 50
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 3:  # y button
                rPillarInitCoord += increment
                lPillarInitCoord += increment
            if event.button == 0:  # a button
                rPillarInitCoord -= increment
                lPillarInitCoord -= increment
            if event.button == 2:  # x button
                neckInitCoord -= increment  # move neck cw
            if event.button == 1:  # b button
                neckInitCoord += increment  # move neck ccw
            if event.button == 4:  # lb
                rPillarInitCoord -= increment
                lPillarInitCoord += increment
            if event.button == 5:  # rb
                rPillarInitCoord += increment
                lPillarInitCoord -= increment
            if event.button == 7:
                hold = True

        # changing the variables that is used to command the servo
        x_axis = joystick_for_eye(xbox.get_axis(0))
        y_axis = joystick_for_eye_r(xbox.get_axis(1))


        # actuate in the test rig
        servo.setTarget(lHorEye, x_axis)
        servo.setTarget(lVertEye, y_axis)
        servo.setTarget(neck, neckInitCoord)
        servo.setTarget(rPillar, rPillarInitCoord)
        servo.setTarget(lPillar, lPillarInitCoord)

    pygame.quit()