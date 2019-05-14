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

#These variables change as the configuration of the robot changes
neckInitCoord = 6000  # faces the front of the test rig
rPillarInitCoord = 5000  # zero head elevation for the right pillar
lPillarInitCoord = 5250  # zero head elevation for the left pillar
eyeHorInitCoord = 3000  # eyes in the middle horizontally
eyeVertInitCoord = 3000  # eyes in the middle vertically


if __name__ == "__main__":
