import datetime
import sched
import time

s = sched.scheduler(time.time, time.sleep)


def event_fun1():
    print("func1 Time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def perform1(inc):
    s.enter(inc, 0, perform1, (inc,))
    event_fun1()


def mymain():
    s.enter(0, 0, perform1, (10,))  # 每隔10秒执行一次perform1


if __name__ == '__main__':
    mymain()
    s.run()
