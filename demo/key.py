#!/usr/bin/env python
#coding: utf-8
from evdev import InputDevice
from select import select

key_name = 0

def detectInputKey():
    global key_name
    dev = InputDevice('/dev/input/event4')
    while True:
        select([dev], [], [])
        for event in dev.read():
            if event.value == 1:
                key_name  = event.code
                print(key_name)

if __name__ == '__main__':
    detectInputKey()