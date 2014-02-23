#!/usr/bin/env python

import time
import fluidsynth

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

fs = fluidsynth.Synth(gain=3)
fs.start()

sfid = fs.sfload("best drums.sf2")
fs.program_select(0, sfid, 0, 0)

def playDrum(drum, velocity):
    fs.noteon(0, drumID[drum], velocity * 8)
    print drumID[drum]

# fs.noteon(0, open_hi_hat, 80)
# fs.noteon(0, cabasa, 127)
# 
# 
# i = 0
# while True:
#     fs.noteon(0, drumID[2], 127)
#     print i
#     i+=1
    # time.sleep(0.5)

# fs.noteoff(0, 60)
# fs.noteoff(0, 67)
# fs.noteoff(0, 76)

# time.sleep(1.0)

# fs.delete()
