import maestro
m = maestro.Controller('COM6')
servo = maestro.Controller()
servo.setAccel(1,4)      #set servo 0 acceleration to 4
servo.setTarget(0,1100)  #set servo to move to center position
servo.setSpeed(1,4)     #set speed of servo 1
x = servo.getPosition(1) #get the current position of servo 1
print(x)
servo.close()