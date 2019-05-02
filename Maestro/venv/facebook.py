# from fbchat import Client
# from fbchat.models import *
# import RoboticEyesMovement
# import os
# client = Client('khrisnaadi@ymail.com', 'Samiaji10bandung')
#
# if __name__ == "__main__":
#     no_of_friends = 1
#     for i in range(no_of_friends):
#         name = "Rachel Krause"
#         friends = client.searchForUsers(name)  # return a list of names
#         friend = friends[0]
#         msg = "Gucci Gang!"
#         for i in range(200):
#             sent = client.send(Message(text=msg), friend.uid, thread_type=ThreadType.USER)
#             if sent:
#                 print("Message sent successfully!")
#
#         # messages = client.fetchThreadMessages(friend.uid, limit=1)
#         # print(messages[0].text)
'''
to do:
1. add rotate neck coordinate transform
'''

from fbchat import Client
from fbchat.models import *
import RoboticEyesMovement
import os
import serial
client = Client('khrisnaadi@gmail.com', 'Samiaji10bandung')

if __name__ == "__main__":
    RoboticEyesMovement.initialize()
    no_of_friends = 1
    for i in range(no_of_friends):
        name = "Khrisna Kamarga"
        friends = client.searchForUsers(name)  # return a list of names
        friend = friends[0]
        msg = "Hello, Neighbor!"
        sent = client.send(Message(text='Starting Robotic Eyes'), friend.uid, thread_type=ThreadType.USER)
        if sent:
            print("Message sent successfully!")

        messages = client.fetchThreadMessages(friend.uid, limit=1)
        print(messages[0].text)

        while True:
            try:
                messages = client.fetchThreadMessages(friend.uid, limit=1)
                command = str(messages[0].text)
                if command.find(" ") != -1:
                    everything = command.split(" ")
                    command = everything[0]
                    x = everything[1]
                    y = everything[2]
                if command == "Run":
                    # os.system("python RoboticEyesMovement.py")
                    RoboticEyesMovement.main()
                    sent = client.send(Message(text='Stop'), friend.uid, thread_type=ThreadType.USER)
                elif command == "Stare":
                    RoboticEyesMovement.stare_to_point(int(x), int(y))
                    sent = client.send(Message(text='Done!'), friend.uid, thread_type=ThreadType.USER)
                elif command == "Initialize":
                    RoboticEyesMovement.initialize()
                    sent = client.send(Message(text='Initialized'), friend.uid, thread_type=ThreadType.USER)
                elif command == "Keyboard":
                    RoboticEyesMovement.keyboard_control_front()
                    sent = client.send(Message(text='Initialized'), friend.uid, thread_type=ThreadType.USER)
                elif command == "Off":
                    RoboticEyesMovement.servos_off()
                    sent = client.send(Message(text='Servos are off'), friend.uid, thread_type=ThreadType.USER)
                elif command == "Neck":
                    RoboticEyesMovement.rotate_neck(int(x))
                    sent = client.send(Message(text='Rotating Neck'), friend.uid, thread_type=ThreadType.USER)
                elif command == 'Bye':
                    sent = client.send(Message(text='See you'), friend.uid, thread_type=ThreadType.USER)
                    exit()

            except (RoboticEyesMovement.maestro.serial.SerialException, IndexError, ValueError) as e:
                sent = client.send(Message(text='Something\'s wrong :('), friend.uid, thread_type=ThreadType.USER)