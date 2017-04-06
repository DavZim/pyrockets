import sys
import pygame
import pygame.time
from pygame.locals import *

from Rectangle import Rectangle

if __name__ == "__main__":

    screen = pygame.display.set_mode((1000,1000), 0, 32)
    screen.fill((0, 0, 0))  # fill black
    pygame.init()
    # FPS = Frames Per Second
    FPSCLOCK = pygame.time.Clock()


    # draw the target circle
    pygame.draw.circle(screen, (255, 0, 0), (500,100), 40, 0)

    # draw the obstacle
    obs1 = Rectangle(500, 700, 50, 300, 00)
    pygame.draw.polygon(screen, (255, 255, 255), obs1.get_pts())

    # draw a simplistic rocket
    rocket1 = Rectangle(500, 975, 50,10)
    pygame.draw.polygon(screen, (0, 0, 255), rocket1.get_pts())

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
        # check exit conditions
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # redraw the screen elements
        screen.fill((0,0,0))
        pygame.draw.polygon(screen, (255, 255, 255), obs1.get_pts())
        scoretext = font.render("Hello World, we are in round %d" % (0), 1, (255, 255, 255))
        screen.blit(scoretext, scoretext.get_rect(center=(500,500)))
        st2 = font.render("below is an obstacle, at the bottom is a rocket, and above is the target",
            1, (255, 255, 255))
        screen.blit(st2, scoretext.get_rect(center=(350,600)))

        # move the rocket upwards by 10 units
        rocket1.move_forwards(-10)
        # check that the rocket is not outside of the screen
        if rocket1.y < 0:
            rocket1.move_to(500, 1000)
        # draw the rocket
        pygame.draw.polygon(screen, (0,0,255), rocket1.get_pts())

        # update the display
        pygame.display.update()

        # wait so long that we achieve 50 FPS
        FPSCLOCK.tick(50)