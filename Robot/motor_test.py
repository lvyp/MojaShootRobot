from comMotor import *
from canMotor import *

emotion_list = [201.08, 208.56, 311.96, 217.8, 273.68, 249.04, 75.68, 195.36, 83.6, 194.92, 93.7, 227.04, 305.8, 94.16, 285.12, 512, 54, 0]
#喜
smile_list = [143.44, 208.56, 311.96, 277.2, 273.68, 249.04, 54.56, 156.64, 137.28, 194.92, 50.16, 227.04, 305.8, 161.92, 285.12, 288, 342.8, 0]
#悲
sad_list = [258.72, 169.84, 343.2, 158.4, 328.24, 194.48, 96.8, 234.08, 29.92, 169.84, 187.44, 189.2, 344.96, 26.4, 285.12, 684, -54, 0]
#怒
argry_list = [258.72, 247.28, 280.72, 158.4, 273.68, 249.04, 54.56, 234.08, 29.92, 220, 187.44, 264.88, 266.64, 26.4, 285.12, 684, -54, 0]
#惊奇
amizing_list = [143.44, 169.84, 343.2, 143.44, 273.68, 249.04, 54.56, 195.36, 83.6, 194.92, 50.16, 189.2, 344.96, 161.92, 247.28, 684, -54, 0]
#挑衅
fight_list = [258.72, 208.56, 311.96, 158.4, 273.68, 221.76, 54.56, 195.36, 83.6, 220, 187.44, 264.88, 266.64, 26.4, 285.12, 684, 342, 0]

mouth_list = [237.68, 249.09, -316.8, -54]
#闭嘴
shutup_list = [300.96, 221.76, -180, 180]
#微张嘴
small_list = [287.32, 235.4, -180, 180]
#大张嘴
large_list = [237.68, 249.09, -180, 180]

#胡子
goatee_list = [184.8, 232.8]

m_comMotor = ComMotor("COM1")
canmotor = CanMotor()

#竹小贱嘴巴动作
def mouth_test(var_list):
    for i in range (2):
        m_comMotor.action(i + 5, float(var_list[i]))

    for i in range(2):
        canmotor.MOTOR_Ctr(i + 16, float(var_list[i + 2]))

#竹老贱嘴巴动作
def mouth_test_old(var):
    m_comMotor.action(15, var)

#表情动作
def emotion_test(var_list):
    for i in range(6):
        m_comMotor.action_speed(i + 1, float(var_list[i]), 100, 50)

    for i in range(9):
        m_comMotor.action_speed(i + 7, float(var_list[i + 6]), 20, 10)

    for i in range(3):
        canmotor.MOTOR_Ctr(i + 16, float(var_list[i + 15]))

#初始化
def motor_init():
    canmotor.RUN_CAN()
    canmotor.MOTOR_INIT(16)
    canmotor.MOTOR_INIT(17)
    canmotor.MOTOR_INIT(18)

if __name__ == '__main__':

    motor_init()

    while 1:

        # emotion_test(smile_list)
        # time.sleep(1)
        #
        # emotion_test(sad_list)
        # time.sleep(1)
        #
        # emotion_test(argry_list)
        # time.sleep(1)
        #
        # emotion_test(amizing_list)
        # time.sleep(1)
        #
        # emotion_test(fight_list)
        # time.sleep(1)

        emotion_test(emotion_list)
        time.sleep(1)
        #
        # mouth_test(shutup_list)
        # time.sleep(1)
        #
        # mouth_test(large_list)
        # time.sleep(1)
        #
        # mouth_test(shutup_list)
        # time.sleep(1)
        #
        # for i in range (10):
        #
        #     mouth_test(small_list)
        #     time.sleep(0.1)
        #
        #     mouth_test(shutup_list)
        #     time.sleep(0.1)
        #
        # for i in range (5):
        #
        #     mouth_test(large_list)
        #     mouth_test_old(float(goatee_list[0]))
        #     time.sleep(0.5)
        #
        #     mouth_test(shutup_list)
        #     mouth_test_old(float(goatee_list[1]))
        #     time.sleep(0.5)





