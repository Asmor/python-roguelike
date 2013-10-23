import pygame.display
import time

picture = pygame.image.load("images/oryx_16bit_fantasy_world_trans.png");

pygame.display.set_mode(picture.get_size())

main_surface = pygame.display.get_surface()
main_surface.blit(picture, (0, 0))
pygame.display.update()

time.sleep(5)

def showSprite(col, row):
	