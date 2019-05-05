currentX = 1
currentY = 1

row = 5   #need to get this set from the UI
col = 5

def get_X():
    return currentX

def get_Y():
    return currentY

def increment_index():
    global currentY
    global currentX
    if currentX/col != 1:
        currentX = currentX + 1
    else:
        currentY = currentY + 1
        currentX = 1


if __name__ == "__main__":
    row = row  #do nothing

