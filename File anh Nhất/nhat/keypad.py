import RPi.GPIO as GPIO
import time

L1 = 5
L2 = 6
L3 = 13
L4 = 19
L5 = 26

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(L5, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

layout0 = [["shift","<",">","del"],
           ["7","8","9","+"],
           ["4","5","6","-"],
           ["1","2","3","*"],
           [".","0","solve","/"]]

layout1 = [["shift","<",">","clr"],
           ["7","8","9","x"],
           ["4","5","6","^"],
           ["1","2","3","="],
           [".","0","solvea","ans"]]
layout = [layout0, layout1]

def readLine(line):
    c = -1
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        c = 0
    if(GPIO.input(C2) == 1):
        c = 1
    if(GPIO.input(C3) == 1):
        c = 2
    if(GPIO.input(C4) == 1):
        c = 3
    GPIO.output(line, GPIO.LOW)
    return c

L = [L1, L2, L3, L4, L5]
def getKey(layoutid):
    for i, l in enumerate(L):
        c = readLine(l)
        if c != -1:
            time.sleep(0.05) 
            if c == readLine(l):
                return layout[layoutid][i][c]



# try:
#     while True:
#         readLine(L1, ["1","2","3","A"])
#         readLine(L2, ["4","5","6","B"])
#         readLine(L3, ["7","8","9","C"])
#         readLine(L4, ["*","0","#","D"])
#         readLine(L5, ["+","-","/","E"])
#         time.sleep(0.1) 
# except KeyboardInterrupt:
#     print("\nApplication stopped!")
