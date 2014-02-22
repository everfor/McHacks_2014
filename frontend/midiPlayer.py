import pygame
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
print "hey I finaly got this working!"
sounds = []
sounds.append(pygame.mixer.Sound('kissMe.mid'))
sounds.append(pygame.mixer.Sound('mary.mid'))
for sound in sounds:
    sound.play()