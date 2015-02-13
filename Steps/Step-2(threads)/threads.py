# -*- coding: utf-8 -*-
# Демо программа с потоками
from threading import Thread
import time


def clock(interval):
    """
    Просто выводим текущее время, через установленный интервал
    """
    while True:
        print("The time is %s" % time.ctime())
        time.sleep(interval)


def print_list(lst, interval):
    """
    Выводим элементы списка, через установленный интервал
    """
    i = 0
    for el in lst:
        print("lst[%s] = %s"%(i, el))
        i+=1
        time.sleep(interval)

th1 = Thread(target=clock, args=(1,))
th2 = Thread(target=print_list, args=([5, -5, 10, 7, 4, 0, 3], 3))
# t.daemon = True
th1.start()
th2.start()
while True:
    pass