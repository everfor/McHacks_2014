#!/usr/bin/env python

import pygame
import pygame.gfxdraw
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

drumImages = [
    "BG",
    "hat",
    "crash1",
    "small",
    "snare",
    "floor",
    "mid",
    "ride",
    "crashg"
]

threads = [None]*16
i = 0


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
    data = struct.unpack('bbb', line)
    drum = data[0]
    velocity = data[1]
    print data
    return drum, velocity


fs = fluidsynth.Synth(gain=3)
fs.start()

sfid = fs.sfload("best drums.sf2")
fs.program_select(0, sfid, 0, 0)


def playDrum(drum, velocity):
    fs.noteon(0, drumID[drum], 127)
    print drumID[drum], "\t", velocity
    # time.sleep(0.1)

# MAIN
try:
    # CONNECT
    ser = connect()

    if __name__ == '__main__':
        pygame.init()
        screen = pygame.display.set_mode((1280, 800))
        background = pygame.image.load('img/BG.png')
        screen.fill((25, 25, 25))
        screen.blit(background, [10, 40])
        pygame.display.flip()

        # FRUIT LOOPS
        while True:
            try:
                # READ SERIAL DATA AND PUBLISH TOPIC
                line = ser.readline().rstrip()

                drum, velocity = parse(line)
                threads[i] = thread.start_new_thread(playDrum, (drum, velocity, ))

                i += 1
                if i == 16:
                    i = 0

                hovering = 'hover' if (velocity <= 0) else 'hit'

                if drum > 0:
                    image = pygame.image.load('img/' + drumImages[drum] + '_' + hovering + '.png')
                    screen.blit(image, [10, 40])
                else:
                    screen.blit(background, [10, 40])

                pygame.display.flip()

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
