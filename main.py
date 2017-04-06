import pygame
import pygame.time
from pygame.locals import *

if __name__ == "__main__":

	screen = pygame.display.set_mode((1000,1000), 0, 32)
	screen.fill((0, 0, 0))  # fill black
	pygame.init()

	# draw the target circle
	pygame.draw.circle(screen, (255, 0, 0), (500,100), 40, 0)

	# draw the obstacle
	pygame.draw.polygon(screen, (255, 255, 255), ((200,675),(200,725),(800,725),(800,675)))

	# draw a simplistic rocket
	pygame.draw.polygon(screen, (0, 0, 255), ((495,950),(505,950),(505,1000),(495,1000)))

	# add some text
	font = pygame.font.Font(None, 30)
	scoretext = font.render("Hello World, we are in round %d" % (0), 1, (255, 255, 255))
	screen.blit(scoretext, scoretext.get_rect(center=(500,500)))

	st2 = font.render("below is an obstacle, at the bottom is a rocket, and above is the target",
		1, (255, 255, 255))
	screen.blit(st2, scoretext.get_rect(center=(350,600)))

	# update the display
	pygame.display.update()

	# game routine: loop that runs until we quit [x]
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()