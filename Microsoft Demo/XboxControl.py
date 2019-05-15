import maestro  # maestro library
import time  # for sleeping
import save_servo_state_left as save_left  # saving left eye calibration map
import save_servo_state_right as save_right  # saving right eye calibration map
import coordinate_gen as cg  # generating the grid for the calibration map

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

# global variables
# States
CALIBRATE = True
CONTROL = False
# initial values of servo middle point
x_axis = 3715
y_axis = 2560

def main():
    initialize()
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

def joystick_proportional_control_right():
    initialize()
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
        x_increment = xbox.get_axis(0)*30
        y_increment = xbox.get_axis(1)*30
        increment = 20
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
        if xbox.get_button(4):  # lb
            rPillarInitCoord -= increment
            lPillarInitCoord += increment
        if xbox.get_button(5):  # rb
            rPillarInitCoord += increment
            lPillarInitCoord -= increment
        if xbox.get_button(6):  # showing the value of servo command
            print(x_axis)
            print(y_axis)
            time.sleep(0.5)  # debounce
        if xbox.get_button(11):  # rt
            save_right.save_state(eyeHorInitCoord, eyeVertInitCoord)
            cg.increment_index()
            time.sleep(0.5)  # debounce
        if xbox.get_button(9):  # right joystick (for resetting the calibration map
            cg.reset()  # start the coordinate from 0, 0
            save_right.reset_everything()  # emptying the calibration matrix

        if xbox.get_button(7):  # start
            cg.reset  # resetting the matrix index
            pygame.quit()
            break

        # changing the variables that is used to command the servo
        if abs(x_increment) > 1:  # cutoff to avoid drifting
            x_axis += x_increment
        if abs(y_increment) > 1:  # cutoff to avoid drifting
            y_axis += y_increment


        # actuate in the test rig
        servo.setTarget(rHorEye, x_axis)
        servo.setTarget(rVertEye, y_axis)
        servo.setTarget(neck, neckInitCoord)
        servo.setTarget(rPillar, rPillarInitCoord)
        servo.setTarget(lPillar, lPillarInitCoord)

    pygame.quit()


# stares at the grid points
# if you want to change the grid geometry, please edit cg and save_servo
def grid():
    col = coordinate_gen.col
    row = coordinate_gen.row
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


def joystick_proportional_control_left():
    initialize()
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

        x_increment = xbox.get_axis(0) * 30
        y_increment = xbox.get_axis(1) * 30
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
        if xbox.get_button(4):  # lb
            rPillarInitCoord -= increment
            lPillarInitCoord += increment
        if xbox.get_button(5):  # rb
            rPillarInitCoord += increment
            lPillarInitCoord -= increment
        if xbox.get_button(6):  # showing the value of servo command
            print(x_axis)
            print(y_axis)
            time.sleep(0.5)  # debounce
        if xbox.get_button(11):  # rt
            save_left.save_state(x_axis, y_axis)
            cg.increment_index()
            time.sleep(0.5)  # debounce
        if xbox.get_button(9):  # right joystick (for resetting the calibration map
            cg.reset()  # start the coordinate from 0, 0
            save_left.reset_everything()  # emptying the calibration matrix
        if xbox.get_button(7):  # start
            cg.reset  # resetting the matrix index
            pygame.quit()
            break

        # actuate in the test rig
        servo.setTarget(lHorEye, x_axis)
        servo.setTarget(lVertEye, y_axis)
        servo.setTarget(neck, neckInitCoord)
        servo.setTarget(rPillar, rPillarInitCoord)
        servo.setTarget(lPillar, lPillarInitCoord)

    pygame.quit()


if __name__ == '__main__':
    joystick_proportional_control_right()
    joystick_proportional_control_left()
    grid()
