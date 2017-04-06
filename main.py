import sys
import pygame
import pygame.time
from pygame.locals import *

from Game import Game
from Rectangle import Rectangle
from Rocket import Rocket

if __name__ == "__main__":

    game = Game(1000, 1000, 100, 300)
    game.run()
