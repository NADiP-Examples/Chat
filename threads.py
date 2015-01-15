import threading
import time
def clock(interval):
    while True:
        print("The time is %s" % time.ctime())
        time.sleep(interval)
t = threading.Thread(target=clock, args=(1,))
t.daemon = True
t.start()
while True:
    print(input(':'))