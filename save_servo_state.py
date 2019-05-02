import user_interface   #get current
import coordinate_gen
import servo_control

'''
Author: Kaiyu Shi
This module:
- save_state() is called when enter key is pressed... is ENTERFLAG redundant?
- gets current servo positions and target coordinates and saves it to array, increments each time the enter key is detected
- at the end saves to a final array to be called by generate_map.

'''

eyechannelx_l = 1
eyechannely_l = 2
eyechannelx_r = 3
eyechannely_r = 4     # standin for eye channels

array_position_l = 0
array_position_r = 0

left_array = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]   # 4 test points, first 2 is servo coordinate, last 2 is X,Y
right_array = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
left_array_final = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
right_array_final = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def save_state():    # we can also have save_state run only when the ENTERFLAG is pressed...
    global array_position_l
    global array_position_r
    global left_array
    global right_array
    global left_array_final
    global right_array_final

    if user_interface.EYEFLAG:      #saving for left eye or right eye
        if array_position_l == 9:
            left_array_final = left_array
        else:
            left_array[array_position_l] = [servo_control.getPos(eyechannelx_l), servo_control.getPos(eyechannely_l), coordinate_gen.x, coordinate_gen.y]
            array_position_l = array_position_l + 1
    else:
        if array_position_r == 9:
            right_array_final = right_array
        else:
            right_array[array_position_r] = [servo_control.getPos(eyechannelx_r), servo_control.getPos(eyechannely_r), coordinate_gen.x, coordinate_gen.y]
            array_position_r = array_position_r + 1
    return


def reset_arrays():
    global left_array
    global right_array
    left_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    right_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    return


