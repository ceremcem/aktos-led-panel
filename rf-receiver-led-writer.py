#!/usr/bin/env python 
# coding: utf-8

import serial
import time
import re
try:
    import crcmod
    crc16 = crcmod.mkCrcFun(0x18005, initCrc=0, xorOut=0)
except:
    print("there is no crcmod module in this machine")

from test import *

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, False)

static_message("aktos")



s = serial.Serial()
#s.port = 'COM3'
s.port = '/dev/ttyAMA0'
s.baudrate = 4800

def hex_from_readable(string):
    string = re.sub(r"[\n\s]+", " ", string)
    chars = [i for i in string.split(" ") if len(i) > 0]
    print "chars: ", chars
    chars_hex = map(lambda x: int(x, 16), chars)
    return ''.join(map(chr, chars_hex))

def readable_from_hex(string):
    l = map(ord, string)
    l = map(lambda x: hex(x)[2:].zfill(2).upper(), l)
    return ' '.join(l)

def is_found(index):
    return index > -1
try:
    s.open()
    buff = ''
    fixed_lenght_of_telegram = 7
    prev_telegram = ''
    last_received_timestamp = time.time()
    while True: 
        recv = s.read(s.inWaiting())
        #print "got packet: ", readable_from_hex(recv)

        buff += recv
        start_index = buff.find("\x01")
        end_index = buff.find("\x04")
        if is_found(start_index) and is_found(end_index):
            if end_index < start_index:
                # beginning is garbage, clear this
                buff = buff[start_index:]
            elif end_index - start_index + 1 == fixed_lenght_of_telegram:
                # check the fixed length
                possible_telegram = buff[start_index:end_index+1]
                #print "possible telegram: ", repr(possible_telegram)
                calculated_crc = crc16(possible_telegram[:-3])
                [x, y] = possible_telegram[-3:-1]
                telegram_crc = ord(x)<<8 | ord(y)

                #print "compare crc:", calculated_crc, repr(telegram_crc)

                timeout_between_telegrams = 1.0  # seconds 
                if calculated_crc == telegram_crc:
                    recv_telegram = possible_telegram

                    if recv_telegram == prev_telegram:
                        if time.time() - last_received_timestamp > timeout_between_telegrams:
                            prev_telegram = ''
                        last_received_timestamp = time.time()

                    if recv_telegram != prev_telegram:
                        button = ''.join(bin(ord(recv_telegram[3]))[2:].zfill(8))
                        print "got telegram: ", readable_from_hex(recv_telegram), '-'.join(button)

                        msg = [
                            'emir asb.',
                            'MESGUL',
                            'Emir Asb.',
                            'Hazirlik',
                            'Aktos',
                            'merhaba',
                        ]

                        remap = [5, 4, 3, 2, 6, 1]

                        print "button has %d digits." % len(button)
                        for k in range(len(button)):
                            if button[k] == '1':
                                try:
                                    static_message(msg[k])
                                except:
                                    static_message('tanimsiz')

                        GPIO.output(4, True)
                        time.sleep(0.2)
                        GPIO.output(4, False)



                    prev_telegram = recv_telegram
                    buff = buff[end_index+1:]
                else:
                    # no telegram detected
                    buff = buff[start_index+1:]


        if len(buff) > 100:
            buff = buff[90:]
            #print "buffer is truncated"
        time.sleep(0.01)
        
finally:
    s.close()
