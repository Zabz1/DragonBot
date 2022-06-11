#from datetime import datetime
from random import randrange
import time

# pip install pure-python-adb
from ppadb.client import Client as AdbClient

# logfilename = 'log.txt'

# def log(content,title=None):
#     header = f'____________________________________________\nLOGGING    {datetime.now()}\n'
#     logstr = f'           {title}\n{content}'
#     print(f'────────────────────────────────────────────\nLOGGING    {datetime.now()}')
#     print(logstr)
#     with open(logfilename, "a") as myfile:
#         myfile.write(header)
#         myfile.write(logstr + '\n')



frequency = 3600*1 # Updatefrequency in s
i = 0 # routine counter
idle_frequency = 10 # after how many routines idle reward should be claimed

def screenshot():
    device.shell("screencap -p /sdcard/screen.png")
    device.pull("/sdcard/screen.png", "screen.png")

def home_btn():
    device.shell("input keyevent KEYCODE_HOME")

def tap(x,y):
    device.shell(f"input tap {x} {y}")

def wait(t):
    print(f"Waiting...{t}s",end=" " ,flush=True)
    time.sleep(t)
    print("... done")

def routine():
    global i

    # wakeup and unlock
    device.shell("input keyevent KEYCODE_WAKEUP")
    device.shell("input keyevent KEYCODE_MENU")
    # reset to known state
    device.shell("input keyevent KEYCODE_HOME")
    
    print("open app")
    tap(540,1700) # open app
    wait(15)
    # landscape orientation switches x/y sometimes
    
    # update confirm
    print("update confirm")
    device.shell("input touchscreen tap 1200 700 ")
    wait(15)

    # patch notes close

    # start
    print("start")
    device.shell("input touchscreen tap 960 860 ")
    wait(10)

    # close announcement
    print("close announcement")
    device.shell("input touchscreen tap 1560 110 ")
    wait(2)

    # sign-in event claim
    print("sign-in event claim")
    device.shell("input touchscreen tap 1390 930 ")
    wait(2)

    # close event
    print("close event")
    device.shell("input touchscreen tap 1850 100 ")
    wait(2)

    # collect statue island ressources
    print("collect statue island ressources")
    device.shell("input touchscreen tap 330 707 ")
    wait(10)

    # collect statue idle
    print("collect statue idle")
    device.shell("input touchscreen tap 455 568 ")
    wait(4)

    # collect statue gem
    print("collect statue idle")
    device.shell("input touchscreen tap 394 633 ")
    wait(4)

    if i >= idle_frequency:
        # Battle
        print("Battle")
        device.shell("input touchscreen tap 110 960 ")
        wait(2)

        # Adventure
        print("Adventure")
        device.shell("input touchscreen tap 340 450 ")
        wait(2)

        # Loot
        print("Loot")
        device.shell("input touchscreen tap 1810 258 ")
        wait(2)

        # Claim
        print("Claim")
        device.shell("input touchscreen tap 960 919 ")
        wait(2)

        # possible levelup
        print("possible levelup")
        device.shell("input touchscreen tap 987 913 ")
        wait(2)

        i = 0

    # close app
    print("close app")
    device.shell("am force-stop com.jdgames.dragon.googleplay")
    wait(2)

    # go to sleep
    print("go to sleep")
    device.shell("input keyevent 26")

def deamon():
    global i

    starttime = time.perf_counter()
    humanrand = randrange(100)

    while True:
        print("DEAMON",f"{round(starttime+frequency+humanrand-time.perf_counter()):5d}",end='\r')
        if starttime <= time.perf_counter() - frequency:
            print("")
            i += 1
            routine()
            humanrand = randrange(100)
            starttime = time.perf_counter()
        time.sleep(1)


# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device = devices[0]
print(device)
deamon()
    





