#!/usr/bin/env python

import string
import datetime
import RPi.GPIO as GPIO
import time

sections = [23,15,11,13,7,16,3,12] #a,b,c,d,e,f,g,dp
tubes = [26,24,21,19] #1,2,3,4
numbers = [
                '0000001','1001111','0010010','0000110','1001100',
                '0100100','0100000','0001111','0000000','0000100'
                ] #0,1,2,3,4,5,6,7,8,9
freq = 0.005
staytime = 5

def setup():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.OUT)  #IO4
        GPIO.setup(11, GPIO.OUT) #IO17
        GPIO.setup(12, GPIO.OUT) #IO18
        GPIO.setup(13, GPIO.OUT) #IO21
        GPIO.setup(15, GPIO.OUT) #IO22
        GPIO.setup(16, GPIO.OUT) #IO23
        GPIO.setup(3, GPIO.OUT)  #SDA0
        GPIO.setup(19, GPIO.OUT) #MOSI
        GPIO.setup(21, GPIO.OUT) #MISO
        GPIO.setup(23, GPIO.OUT) #SCLK
        GPIO.setup(24, GPIO.OUT) #CE0
        GPIO.setup(26, GPIO.OUT) #CE1
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(26, GPIO.LOW)

def tubeon(loc):
        GPIO.output(tubes[loc], GPIO.HIGH)

def tubeoff(loc):
        GPIO.output(tubes[loc], GPIO.LOW)

def clearmod():
        for mod in sections:
                GPIO.output(mod, GPIO.HIGH)
        time.sleep(0.001)

def setmod(num, dp=False):
        numstr = numbers[num]
        clearmod()
        i = 0
        for mod in sections:
                if i<7:
                        if (string.atoi(numstr[i]) == 0):
                                GPIO.output(mod, GPIO.LOW)
                else:
                        if dp:
                                GPIO.output(mod, GPIO.LOW)
                i += 1

def setnumber(numstr, dpLoc=5):
        if len(numstr)<4:
                for i in range(0, 4-len(numstr)):
                        numstr = '0'+numstr
        for i in range(0, 4):
                tubeon(i)
                dp = False
                if i == dpLoc:
                         dp = True
                setmod(string.atoi(numstr[i]), dp)
                time.sleep(freq)
                tubeoff(i)

def gettimestr(t):
        ts = str(t.tm_hour)
        if t.tm_min < 10:
                ts  += '0'
        ts += str(t.tm_min)
        return ts

def showtime():
        t = time.localtime()
        dpLoc = 1
        if t.tm_sec % 2 == 0:
                dpLoc = 1
        setnumber(gettimestr(t), dpLoc)

def timeout(s):
        t = time.time()
        return int((t-s)/staytime)%2 > 0

if __name__ == "__main__":
        start = time.time()
        try:
                setup()
                while True:
                        f = file('digital.dat')
                        line = f.readline()
                        f.close()
                        if len(line) == 0 or timeout(start):
                                showtime()
                        else:
                                setnumber(line)
        except Exception, x:
                print(x)
                for i in range(0, 4):
                        tubeoff(i)
        finally:
                GPIO.cleanup()
