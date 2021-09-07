import threading
import time, random
from multiprocessing import Process, Semaphore

def ktv(sem):
    sem.acquire()
    print('%s 走出ktv')

def ktv_in(sem):
    str = input("input")
    print('%s 走进ktv')
    sem.release()

if __name__ == "__main__":
    sem = Semaphore()
    p = Process(target=ktv, args=(sem, ))
    p.start()
    s = threading.Thread(target=ktv_in, args=(sem, ))
    s.start()