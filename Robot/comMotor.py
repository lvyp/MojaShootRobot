#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available SCServo model on this example : All models using Protocol SCS
# This example is tested with a SCServo(STS/SMS/SCS), and an URT
# Be sure that SCServo(STS/SMS/SCS) properties are already set as %% ID : 1 / Baudnum : 6 (Baudrate : 1000000)
#

import os

from scservo_sdk import COMM_SUCCESS


if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
        
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from scservo_sdk import *                    # Uses SCServo SDK library
def FACE_1():
    # Control table address
    ADDR_SCS_TORQUE_ENABLE     = 40     # 0x28
    ADDR_SCS_GOAL_ACC          = 41     # 0x29
    ADDR_SCS_GOAL_POSITION     = 42     # 0x2A
    ADDR_SCS_GOAL_SPEED        = 46     # 0x2E
    ADDR_SCS_PRESENT_POSITION  = 56     # 0x38

    # Default setting
    SCS_ID                      = 1                 # SCServo ID : 1
    BAUDRATE                    = 115200           # SCServo default baudrate : 1000000
    DEVICENAME                  = 'COM6'    # Check which port is being used on your controller
                                                    # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

    SCS_MINIMUM_POSITION_VALUE  = 100         # SCServo will rotate between this value
    SCS_MAXIMUM_POSITION_VALUE  = 2000        # and this value (note that the SCServo would not move when the position value is out of movable range. Check e-manual about the range of the SCServo you use.)
    SCS_MOVING_STATUS_THRESHOLD = 20          # SCServo moving status threshold
    SCS_MOVING_SPEED            = 1000           # SCServo moving speed
    SCS_MOVING_ACC              = 100           # SCServo moving acc
    protocol_end                = 2000           # SCServo bit end(STS/SMS=0, SCS=1)

    index = 0
    scs_goal_position = [SCS_MINIMUM_POSITION_VALUE, SCS_MAXIMUM_POSITION_VALUE]         # Goal position


    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Get methods and members of Protocol
    packetHandler = PacketHandler(protocol_end)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        # getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        # getch()
        quit()

    # Write SCServo acc
    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(portHandler, SCS_ID, ADDR_SCS_GOAL_ACC, SCS_MOVING_ACC)
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    elif scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))

    # Write SCServo speed
    scs_comm_result, scs_error = packetHandler.write2ByteTxRx(portHandler, SCS_ID, ADDR_SCS_GOAL_SPEED, SCS_MOVING_SPEED)
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    elif scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))



    for item in range(2):
        print("Press any key to continue! (or press ESC to quit!)")
        # print(getch())
        # if getch() == chr(0x1b):
        #     break
        print("test 123")

        # Write SCServo goal position
        scs_comm_result, scs_error = packetHandler.write2ByteTxRx(portHandler, SCS_ID, ADDR_SCS_GOAL_POSITION, scs_goal_position[index])
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))
        scs_present_position_speed, scs_comm_result, scs_error = packetHandler.read4ByteTxRx(portHandler, SCS_ID, ADDR_SCS_PRESENT_POSITION)
        scs_present_position = SCS_LOWORD(scs_present_position_speed)
        scs_present_speed = SCS_HIWORD(scs_present_position_speed)
        print("[ID:%03d] GoalPos:%03d PresPos:%03d PresSpd:%03d"
           % (SCS_ID, scs_goal_position[index], scs_present_position, SCS_TOHOST(scs_present_speed, 15)))
        #
        #     # if not (abs(scs_goal_position[index] - scs_present_position_speed) > SCS_MOVING_STATUS_THRESHOLD):
        #         break

        time.sleep(2)
        # Change goal position
        if index == 0:
            index = 1
        else:
            index = 0

    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(portHandler, SCS_ID, ADDR_SCS_TORQUE_ENABLE, 0)
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    elif scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
    # Close port
    portHandler.closePort()

if __name__ == '__main__':
    FACE_1()