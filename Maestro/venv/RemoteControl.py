import maestro  # maestro library
import time  # for sleeping
import RoboticEyesMovement  # to get all the methods
import pygame
pygame.init()


joysticks = []
clock = pygame.time.Clock()

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    print("Detected Joystick '", joysticks[-1].get_name(), "'")

xbox = joysticks[-1]



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


if __name__ == "__main__":
    initialize()

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    # eye = RightEye()
    # servo.setTarget(lHorEye, eye.left)
    # # time.sleep(1)
    # servo.setTarget(lVertEye, 2560)
    # time.sleep(1)
    while True:
        x_axis = xbox.get_axis(0)
        print(xbox.get_axis(0))
        servo.setTarget(lHorEye, joystick_for_eye(x_axis))


