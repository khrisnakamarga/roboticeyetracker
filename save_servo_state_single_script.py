import user_interface   #get current
import coordinate_gen
import numpy as np
import csv


'''
Author: Kaiyu Shi
This module:
- save_state() is called when enter key is pressed... no flags involved
- gets current servo positions and target coordinates and saves it to array defined by col and row constants, increments each time the enter key is detected
- at the end saves to a final array that is in the correct format, to a csv.
'''

eyechannelx_l = 1   # channel number of eye servos
eyechannely_l = 2

row = 10     # change array size here
col = 20
last = row*col

array_position_l = 1    #

left_array = []   # array to store data 4 variables in each part, first 2 is servo coordinate hor, vert, last 2 is X,Y coordinate

left_array_final_x = [[[] for i in range(col)] for j in range(row)]   # final array to be saved to csv, and to also be used for interpolation
left_array_final_y = [[[] for i in range(col)] for j in range(row)]

def save_state(index_x,index_y):    # every time this is called it adds to the list
    global array_position_l         # need these to be persistent
    global left_array

    left_array.append([np.random.random()*1000, np.random.random()*1000+2000, index_x, index_y])
    array_position_l = array_position_l + 1

    if array_position_l == last+1:
        save_to_final()
        export_to_csv()
    return

def save_to_final():
    global left_array_final_x
    global left_array_final_y

    for z in range(last):
        left_array_final_x[left_array[z][3-1]-1][left_array[z][4-1]-1] = left_array[z][1-1]
        left_array_final_y[left_array[z][3 - 1] - 1][left_array[z][4 - 1] - 1] = left_array[z][2 - 1]

def export_to_csv():

    with open('testx.csv', 'w', newline='') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(left_array_final_x)

    with open('testy.csv', 'w', newline='') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(left_array_final_y)


def reset_everything():
    global array_position_l
    global left_array
    global left_array_final_x
    global left_array_final_y

    left_array = []
    left_array_final_x = [[[] for i in range(col)] for j in range(row)]  # final array to be saved to csv, and to also be used for interpolation
    left_array_final_y = [[[] for i in range(col)] for j in range(row)]
    array_position_l = 1

    return


if __name__ == "__main__":   #testing
    for i in range(row):
        for j in range(col):
            save_state(i+1,j+1)

    print(left_array_final_x)
    print(left_array_final_y)
