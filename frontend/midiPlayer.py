#!/usr/bin/env python

import serial
import struct
import time
import thread
import fluidsynth

TEENSY_PATH = "/dev/tty.usbmodem10131"  # 'dev/teensy'

no_drum = 0

closed_hi_hat = 42
open_hi_hat = 46
pedal_hi_hat = 44

crash_cymbal_1 = 49

crash_cymbal_2 = 57

low_floor_tom = 41
high_floor_tom = 43

low_mid_tom = 47
hi_mid_tom = 48

snare_drum_rod = 91
snare_drum_brush = 93

ride_cymbal_1 = 51
ride_cymbal_2 = 59

drumID = [
    no_drum,
    open_hi_hat,
    crash_cymbal_1,
    low_mid_tom,
    snare_drum_brush,
    low_floor_tom,
    hi_mid_tom,
    ride_cymbal_1,
    crash_cymbal_2
]

# threads = [None]*16
# i = 0


# # ESTABLISH CONNECTION
# def connect():

#     print 'connecting to teensy...'

#     # KEEP TRYING UNTIL WORKS
#     done = False
#     while not done:
#         try:
#             ser = serial.Serial(TEENSY_PATH)
#             done = True
#         except serial.serialutil.SerialException:
#             print 'connection failed'
#             time.sleep(1)

#     print 'connected!'

#     return ser


# def parse(line):
#     data = struct.unpack('bbb', line)
#     drum = data[0]
#     velocity = data[1]

#     return drum, velocity


fs = fluidsynth.Synth(gain=3)
fs.start()

sfid = fs.sfload("best drums.sf2")
fs.program_select(0, sfid, 0, 0)


def playDrum(drum, velocity):
    fs.noteon(0, drumID[drum], 127)
    print drumID[drum], "\t", velocity
    time.sleep(0.1)

for i in xrange(35, 81):
    fs.noteon(0, i, 127)
    time.sleep(0.1)


# # MAIN
# try:
#     # CONNECT
#     ser = connect()

#     # FRUIT LOOPS
#     while True:
#         try:
#             # READ SERIAL DATA AND PUBLISH TOPIC
#             line = ser.readline().rstrip()

#             drum, velocity = parse(line)
#             threads[i] = thread.start_new_thread(playDrum, (drum, velocity, ))

#             i += 1
#             if i == 16:
#                 i = 0

#         except serial.serialutil.SerialException:
#             # PEACE OUT IF CONNECTION DROPS
#             print 'connection dropped'
#             time.sleep(1)
#             print 'exiting...'
#             fs.delete()
#             exit(1)

# except KeyboardInterrupt:
#     # CTRL-C FRIENDLY
#     print ''
#     print 'goodbye!'
#     ser.close()
#     fs.delete()
#     time.sleep(1)
#     exit(0)
