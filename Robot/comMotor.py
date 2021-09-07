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
import threading

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

# Control table address
ADDR_SCS_TORQUE_ENABLE = 40  # 0x28
ADDR_SCS_GOAL_ACC = 41  # 0x29
ADDR_SCS_GOAL_POSITION = 42  # 0x2A
ADDR_SCS_GOAL_SPEED = 46  # 0x2E
ADDR_SCS_PRESENT_POSITION = 56  # 0x38

BAUDRATE = 115200  # SCServo default baudrate : 1000000
DEVICENAME = 'COM1'  # Check which port is being used on your controller
# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
protocol_end = 2000  # SCServo bit end(STS/SMS=0, SCS=1)



def bitOperation(number):
    return ((number & 0xFF00) >> 8) | ((number & 0xFF) << 8)


class ComMotor(object):

    def __init__(self, com):
        self.scsId = 0
        self.portHandler = None
        self.packetHandler = None
        self.createPacketHandler(com)

    def createPacketHandler(self, com):
        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.portHandler = PortHandler(com)

        # Initialize PacketHandler instance
        # Get methods and members of Protocol
        self.packetHandler = PacketHandler(protocol_end)

        # Open port
        if self.portHandler.openPort():
            # print("Succeeded to open the port")
            pass
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            quit()

        # Set port baudrate
        if self.portHandler.setBaudRate(BAUDRATE):
            # print("Succeeded to change the baudrate")
            pass
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            quit()

    def close(self, SCS_ID):
        scs_comm_result, scs_error = self.packetHandler.write1ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_TORQUE_ENABLE, 0)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(scs_error))
        # Close port
        self.portHandler.closePort()

    def action(self, SCS_ID, degree):
        try:
            SCS_MINIMUM_POSITION_VALUE  = int(float(degree)/0.088)       # SCServo will rotate between this value  (0 - 16)
            SCS_MOVING_SPEED            = 1000           # SCServo moving speed
            SCS_MOVING_ACC              = 100           # SCServo moving acc

            strL = bitOperation(SCS_MINIMUM_POSITION_VALUE)
            # print(str(strL))

            # Write SCServo acc
            scs_comm_result, scs_error = self.packetHandler.write1ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_GOAL_ACC, SCS_MOVING_ACC)
            if scs_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
            elif scs_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(scs_error))

            # Write SCServo speed
            scs_comm_result, scs_error = self.packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_GOAL_SPEED, SCS_MOVING_SPEED)
            if scs_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
            elif scs_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(scs_error))

            # print("test 123")

            # Write SCServo goal position
            scs_comm_result, scs_error = self.packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_GOAL_POSITION, strL)
            if scs_comm_result != COMM_SUCCESS:
                print("SCS_ID>" + str(SCS_ID))
                print("scs_comm_result>" + str(scs_comm_result))
                print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
            elif scs_error != 0:
                print("scs_error>" + str(scs_error))
                print("%s" % self.packetHandler.getRxPacketError(scs_error))
            # scs_present_position_speed, scs_comm_result, scs_error = self.packetHandler.read4ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_PRESENT_POSITION)
            # scs_present_position = SCS_LOWORD(scs_present_position_speed)
            # scs_present_speed = SCS_HIWORD(scs_present_position_speed)
            # print("[ID:%03d] GoalPos:%03d PresPos:%03d PresSpd:%03d"
            #    % (SCS_ID, bitOperation(strL)*0.088, bitOperation(scs_present_position)*0.088, SCS_TOHOST(scs_present_speed, 15)))
            # time.sleep(0.05)
        except Exception as e:
            print("comMotor action >>" + str(e))

    def action_speed(self, SCS_ID, degree, speed, acc):

        #print("SCS_ID>" + str(SCS_ID))
        SCS_MINIMUM_POSITION_VALUE  = int(float(degree)/0.088)       # SCServo will rotate between this value  (0 - 16)
        SCS_MOVING_SPEED            = speed           # SCServo moving speed
        SCS_MOVING_ACC              = acc           # SCServo moving acc

        strL = bitOperation(SCS_MINIMUM_POSITION_VALUE)
        # print(str(strL))

        # Write SCServo acc
        scs_comm_result, scs_error = self.packetHandler.write1ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_GOAL_ACC, SCS_MOVING_ACC)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(scs_error))

        # Write SCServo speed
        scs_comm_result, scs_error = self.packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_GOAL_SPEED, SCS_MOVING_SPEED)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(scs_error))

        # print("test 123")

        # Write SCServo goal position
        scs_comm_result, scs_error = self.packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_GOAL_POSITION, strL)
        if scs_comm_result != COMM_SUCCESS:
            print("scs_comm_result>" + str(scs_comm_result))
            print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("scs_error>" + str(scs_error))
            print("%s" % self.packetHandler.getRxPacketError(scs_error))
        # scs_present_position_speed, scs_comm_result, scs_error = self.packetHandler.read4ByteTxRx(self.portHandler, SCS_ID, ADDR_SCS_PRESENT_POSITION)
        # scs_present_position = SCS_LOWORD(scs_present_position_speed)
        # scs_present_speed = SCS_HIWORD(scs_present_position_speed)
        # print("[ID:%03d] GoalPos:%03d PresPos:%03d PresSpd:%03d"
        #    % (SCS_ID, bitOperation(strL)*0.088, bitOperation(scs_present_position)*0.088, SCS_TOHOST(scs_present_speed, 15)))
        # time.sleep(0.05)


if __name__ == '__main__':
    m_comMotor = ComMotor("COM1")
    while 1:
        m_comMotor.action(5, 300.96)
        m_comMotor.action(6, 221.76)
        time.sleep(0.5)
        m_comMotor.action(5, 287.32)
        m_comMotor.action(6, 235.4)
        time.sleep(0.5 )
    # m_comMotor.action(1, 0)
    # m_comMotor.close(1)
