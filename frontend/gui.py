import pygame
import pygame.gfxdraw

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280,800),pygame.FULLSCREEN)
    backrgound = pygame.image.load('img/BG.png')
    drum = pygame.image.load('img/crash1_hit.png')
    screen.fill((25,25,25))
    screen.blit(backrgound, [10, 40])
    pygame.display.flip()
    try:
        while 1:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
                if event.unicode == 'a':
                    screen.blit(drum, [10, 40])
            else:
                screen.blit(backrgound, [10, 40])
            pygame.display.flip()
    finally:
        pygame.quit()
