import user_interface   #get current
import coordinate_gen
import numpy as np
import csv


'''
Author: Kaiyu Shi
This module:
    tbd
'''

row = 4     # to do: need to get this set from the UI
col = 6
last = row*col

array_position = 1    #not 0

array = []   # array to store data 4 variables in each part, first 2 is servo coordinate hor, vert, last 2 is X,Y coordinate

array_final_x = [[[] for i in range(col)] for j in range(row)]   # final array to be saved to csv, and to also be used for interpolation
array_final_y = [[[] for i in range(col)] for j in range(row)]

def save_state(servo_x,servo_y):    # every time this is called it adds to the list
    global array_position         # need these to be persistent
    global array

    array.append([servo_x, servo_y, coordinate_gen.get_X(), coordinate_gen.get_Y()])
    array_position = array_position + 1
    print("now doing:")
    print(array_position)

    if array_position == last+1:
        save_to_final()
        export_to_csv()
    return

def save_to_final():
    global final_x
    global final_y

    print(array)

    for z in range(last):
        array_final_x[array[z][3-1]-1][array[z][4-1]-1] = array[z][1-1]                 #saves to array using generated X and Y as list indices
        array_final_y[array[z][3 - 1] - 1][array[z][4 - 1] - 1] = array[z][2 - 1]

def export_to_csv():

    with open('left_x.csv', 'w', newline='') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(array_final_x)

    with open('left_y.csv', 'w', newline='') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(array_final_y)


def reset_everything():
    global array_position
    global array
    global array_final_x
    global array_final_y

    array = []
    array_final_x = [[[] for i in range(col)] for j in range(row)]  # final array to be saved to csv, and to also be used for interpolation
    array_final_y = [[[] for i in range(col)] for j in range(row)]
    array_position = 1

    return


def get_row():
    return row


def get_col():
    return col

if __name__ == "__main__":   #testing
    for i in range(row):
        for j in range(col):
            save_state(i+1,j+1)

    print(array_final_x)
    print(array_final_y)
