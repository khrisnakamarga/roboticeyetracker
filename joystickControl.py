import keyboard

def joystickControl():
    UP = 0
    DOWN = 0
    LEFT = 0
    RIGHT = 0

    if keyboard.is_pressed():
        UP = 1
    if keyboard.is_pressed():
        DOWN = 1
    if keyboard.is_pressed():
        LEFT = 1
    if keyboard.is_pressed():
        RIGHT = 1
    output = [UP, DOWN, LEFT, RIGHT]
    return output







