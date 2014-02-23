#!/usr/bin/env python

import pygame
import pygame.gfxdraw
import serial
import struct
import time
from pygame.locals import *
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

drumImages = [
    "BG",
    "hat",
    "crash1",
    "small",
    "snare",
    "floor",
    "mid",
    "ride",
    "crash2"
]

drum = 0
velocity = 0

prevImg = ''


# ESTABLISH CONNECTION
def connect():

    print 'connecting to teensy...'

    # KEEP TRYING UNTIL WORKS
    done = False
    while not done:
        try:
            ser = serial.Serial(TEENSY_PATH)
            done = True
        except:  # serial.serialutil.SerialException:
            print 'connection failed'
            time.sleep(1)

    print 'connected!'

    return ser


def parse(line):
    if len(line) != 3:
        return 0, 0
        
    data = struct.unpack('bbb', line)
    drum = data[0]
    velocity = data[1]
    # print data
    return drum, velocity


fs = fluidsynth.Synth(gain=3)
fs.start()

sfid = fs.sfload("best drums.sf2")
fs.program_select(0, sfid, 0, 0)


def playDrum(drum, velocity):
    fs.noteon(0, drumID[drum], 127)
    time.sleep(0.2)
    # print drumID[drum], "\t", velocity
    # time.sleep(0.1)

# MAIN
try:
    # CONNECT
    ser = connect()

    # thread.start_new_thread(gui, () )
    i = 0
    j = 0
    k = 0

    velocities = [0] * 5
    velocityAvg = [0] * 5
    velocityDiff = [0] * 2

    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    background = pygame.image.load('img/BG.png')
    screen.fill((25, 25, 25))
    screen.blit(background, [10, 40])
    pygame.display.flip()
    pygame.display.set_caption("my window")
    pygame.event.set_allowed(None)

    # FRUIT LOOPS
    while True:
        try:
            pygame.event.pump()

            # READ SERIAL DATA AND PUBLISH TOPIC
            line = ser.readline().rstrip()
            drum, velocity = parse(line)

            velocities[i] = velocity
            velocity = sum(velocities) / 5
            velocityAvg[j] = velocity

            velocityDiff[k] = 2 * velocityAvg[j] + velocityAvg[j - 1] - velocityAvg[j - 3] - 2 * velocityAvg[j - 4]

            if (velocityDiff[k] > 0 and velocityDiff[k - 1] < 0) or (velocityDiff[k] < 0 and velocityDiff[k - 1] > 0):
                playDrum(drum, velocity)

            i += 1
            j += 1
            k += 1

            if i == 5:
                i = 0

            if j == 5:
                j = 0

            if k == 2:
                k = 0

            hovering = 'hover' if (velocity <= 0) else 'hit'

            img = drumImages[drum] + '_' + hovering + '.png'

            if drum == 0:
                img = 'BG.png'

            if not prevImg is img:
                image = pygame.image.load('img/' + img)
                screen.blit(image, [10, 40])
                pygame.display.update()

            prevImg = img

        except serial.serialutil.SerialException:
            # PEACE OUT IF CONNECTION DROPS
            print 'connection dropped'
            time.sleep(1)
            ser.close()
            print 'exiting...'
            fs.delete()
            exit(1)

except KeyboardInterrupt:
    # CTRL-C FRIENDLY
    print ''
    print 'goodbye!'
    ser.close()
    fs.delete()
    pygame.quit()
    time.sleep(1)
    exit(0)
