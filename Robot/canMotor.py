# python3.8.0 64位（python 32位要用32位的DLL）
#
import time
from ctypes import *
#默认
VCI_USBCAN2 = 4
STATUS_OK = 1


class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_uint),
                ("AccMask", c_uint),
                ("Reserved", c_uint),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)
                ]


class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte * 8),
                ("Reserved", c_ubyte * 3)
                ]


CanDLLName = './ControlCAN.dll'  # 把DLL放到对应的目录下
canDLL = windll.LoadLibrary('./ControlCAN.dll')

TIME_OUT = 1


class CanMotor(object):

    def RUN_CAN(self):
        ret = canDLL.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
        if ret == STATUS_OK:
            # print('调用 VCI_OpenDevice成功\r\n')
            pass
        if ret != STATUS_OK:
            print('调用 VCI_OpenDevice出错\r\n')

        # 初始0通道
        vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0,
                                         0, 0x00, 0x14, 0)  # 波特率1000k，正常模式
        ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 0, byref(vci_initconfig))
        if ret == STATUS_OK:
            # print('调用 VCI_InitCAN1成功\r\n')
            pass
        if ret != STATUS_OK:
            print('调用 VCI_InitCAN1出错\r\n')

        ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 0)
        if ret == STATUS_OK:
            # print('调用 VCI_StartCAN1成功\r\
            pass
        if ret != STATUS_OK:
            print('调用 VCI_StartCAN1出错\r\n')

        # 初始1通道
        ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 1, byref(vci_initconfig))
        if ret == STATUS_OK:
            # print('调用 VCI_InitCAN2 成功\r\n')
            pass
        if ret != STATUS_OK:
            print('调用 VCI_InitCAN2 出错\r\n')

        ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 1)
        if ret == STATUS_OK:
            # print('调用 VCI_StartCAN2 成功\r\n')
            pass
        if ret != STATUS_OK:
            print('调用 VCI_StartCAN2 出错\r\n')


    def MOTOR_INIT(self, MOTOR_ADDR):
        # 通道1发送数据
        ubyte_array = c_ubyte * 8
        a = ubyte_array(0x40, 0x0c, 0x20, 0x02, 0x00, 0x00, 0x00, 0x00)
        ubyte3_array = c_ubyte * 3
        b = ubyte3_array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ((0x600 + MOTOR_ADDR), 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == STATUS_OK:
            # print('CAN1通道_1发送成功\r\n')
            pass
        if ret != STATUS_OK:
            print('CAN1通道_1发送失败\r\n')

        time.sleep(0.1)

        ubyte_array = c_ubyte * 8
        a = ubyte_array(0x2b, 0x40, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00)
        ubyte3_array = c_ubyte * 3
        b = ubyte3_array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ((0x600 + MOTOR_ADDR), 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == STATUS_OK:
            # print('CAN1通道_2发送成功\r\n')
            pass
        if ret != STATUS_OK:
            print('CAN1通道_2发送失败\r\n')

        time.sleep(0.1)

        ubyte_array = c_ubyte * 8
        if MOTOR_ADDR == 18:
            a = ubyte_array(0x2b, 0x86, 0x60, 0x00, 0x03, 0x00, 0x00, 0x00)
        else:
            a = ubyte_array(0x2b, 0x86, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00)
        ubyte3_array = c_ubyte * 3
        b = ubyte3_array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ((0x600 + MOTOR_ADDR), 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == STATUS_OK:
            # print('CAN1通道_3发送成功\r\n')
            pass
        if ret != STATUS_OK:
            print('CAN1通道_3发送失败\r\n')

        time.sleep(0.1)

        ubyte_array = c_ubyte * 8
        a = ubyte_array(0x2b, 0x40, 0x60, 0x00, 0x06, 0x00, 0x00, 0x00)
        ubyte3_array = c_ubyte * 3
        b = ubyte3_array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ((0x600 + MOTOR_ADDR), 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == STATUS_OK:
            # print('CAN1通道_8发送成功\r\n')
            pass
        if ret != STATUS_OK:
            print('CAN1通道_8发送失败\r\n')

        time.sleep(0.1)

        ubyte_array = c_ubyte * 8
        a = ubyte_array(0x2b, 0x60, 0x60, 0x00, 0x01, 0x00, 0x00, 0x00)
        ubyte3_array = c_ubyte * 3
        b = ubyte3_array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ((0x600 + MOTOR_ADDR), 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == STATUS_OK:
            # print('CAN1通道_9发送成功\r\n')
            pass
        if ret != STATUS_OK:
            print('CAN1通道_9发送失败\r\n')

        time.sleep(0.1)

        ubyte_array = c_ubyte * 8
        a = ubyte_array(0x2b, 0x40, 0x60, 0x00, 0x80, 0x00, 0x00, 0x00)
        ubyte3_array = c_ubyte * 3
        b = ubyte3_array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ((0x600 + MOTOR_ADDR), 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == STATUS_OK:
            # print('CAN1通道_10发送成功\r\n')
            pass
        if ret != STATUS_OK:
            print('CAN1通道_10发送失败\r\n')

        time.sleep(0.1)

        ubyte_array = c_ubyte * 8
        a = ubyte_array(0x2b, 0x40, 0x60, 0x00, 0x06, 0x00, 0x00, 0x00)
        ubyte3_array = c_ubyte * 3
        b = ubyte3_array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ((0x600 + MOTOR_ADDR), 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == STATUS_OK:
            # print('CAN1通道_11发送成功\r\n')
            pass
        if ret != STATUS_OK:
            print('CAN1通道_11发送失败\r\n')

        time.sleep(0.1)

        ubyte_array = c_ubyte * 8
        a = ubyte_array(0x2b, 0x40, 0x60, 0x00, 0x0F, 0x00, 0x00, 0x00)
        ubyte3_array = c_ubyte * 3
        b = ubyte3_array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ((0x600 + MOTOR_ADDR), 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == STATUS_OK:
            # print('CAN1通道_12发送成功\r\n')
            pass
        if ret != STATUS_OK:
            print('CAN1通道_12发送失败\r\n')

    def MOTOR_Ctr(self, MOTOR_ADDR, POS):

        try:
            POS = float(POS)
            if MOTOR_ADDR == 18:
                POS = int(POS/0.0018)
            else:
                POS = int(POS/0.036)

            ubyte_array = c_ubyte * 8

            send1 = POS & 0x000000ff
            send2 = POS >> 8 & 0x000000ff
            send3 = POS >> 16 & 0x000000ff
            send4 = POS >> 24 & 0x000000ff
            a = ubyte_array(0x23, 0x7A, 0x60, 0x00, send1, send2, send3, send4)
            ubyte3_array = c_ubyte * 3
            b = ubyte3_array(0, 0, 0)
            vci_can_obj = VCI_CAN_OBJ(0x600 + MOTOR_ADDR, 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
            ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
            if ret == STATUS_OK:
                # print('CAN1通道_14发送成功\r\n')
                pass
            if ret != STATUS_OK:
                print('CAN1通道_14发送失败\r\n')
                pass
            time.sleep(TIME_OUT/50)

            ubyte_array = c_ubyte * 8
            if MOTOR_ADDR == 19:
                a = ubyte_array(0x2B, 0x40, 0x60, 0x00, 0x0F, 0x00, 0x00, 0x00)
            else:
                a = ubyte_array(0x2B, 0x40, 0x60, 0x00, 0x2F, 0x00, 0x00, 0x00)
            ubyte3_array = c_ubyte * 3
            b = ubyte3_array(0, 0, 0)
            vci_can_obj = VCI_CAN_OBJ(0x600 + MOTOR_ADDR, 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
            ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
            if ret == STATUS_OK:
                # print('CAN1通道_15发送成功\r\n')
                pass
            if ret != STATUS_OK:
                print('CAN1通道_15发送失败\r\n')
                pass
            time.sleep(TIME_OUT/50)

            ubyte_array = c_ubyte * 8
            if MOTOR_ADDR == 19:
                a = ubyte_array(0x2B, 0x40, 0x60, 0x00, 0x1F, 0x00, 0x00, 0x00)
            else:
                a = ubyte_array(0x2B, 0x40, 0x60, 0x00, 0x3F, 0x00, 0x00, 0x00)
            ubyte3_array = c_ubyte * 3
            b = ubyte3_array(0, 0, 0)
            vci_can_obj = VCI_CAN_OBJ(0x600 + MOTOR_ADDR, 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
            ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
            if ret == STATUS_OK:
                # print('CAN1通道_16发送成功\r\n')
                pass
            if ret != STATUS_OK:
                print('CAN1通道_16发送失败\r\n')
                pass
            time.sleep(TIME_OUT/30)
        except Exception as e:
            print("canMotor Ctr >> " + str(e))


if __name__ == '__main__':
    canmotor = CanMotor()
    canmotor.RUN_CAN()
    canmotor.MOTOR_INIT(16)
    canmotor.MOTOR_INIT(17)
    canmotor.MOTOR_INIT(18)

    if 0:
        while True:
            canmotor.MOTOR_Ctr(17, -54)
            # time.sleep(TIME_OUT)
            canmotor.MOTOR_Ctr(16, 288)
            print("1")
            time.sleep(TIME_OUT)
            canmotor.MOTOR_Ctr(17, 342)
            # time.sleep(TIME_OUT)
            canmotor.MOTOR_Ctr(16, 500)
            print("2")
            time.sleep(TIME_OUT)
    else:
        i = 90
        while True:
            canmotor.MOTOR_Ctr(18, i)
            # canmotor.MOTOR_Ctr(18, i)
            time.sleep(TIME_OUT*4)
            # canmotor.MOTOR_Ctr(18, -i)
            # time.sleep(TIME_OUT * 0.005)
            # i += 10
            # if i >= 170:
            #     i = -170
            # else:
            #     i = 170
            print(i)
            i *= -1



    canDLL.VCI_CloseDevice(VCI_USBCAN2, 0)
