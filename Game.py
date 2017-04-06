import pygame
import pygame.time
from pygame.locals import *
import random, sys

from Rectangle import Rectangle
from Rocket import Rocket
from DNA import DNA


class Game(object):

    # inits a new game, given the x and y dimensions of the screen, the number of rockets and the lifespan of the game
    def __init__(self, xDim, yDim, n_rockets, lifespan):
        # init game
        self.gameSize = (xDim, yDim)
        self.lifespan = lifespan
        self.generation = 0

        pygame.init()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode(self.gameSize, 0, 32)
        self.screen.fill((0, 0, 0))  # fill black

        # FPS = Frames Per Second
        self.FPSCLOCK = pygame.time.Clock()

        # init target
        self.targetPos = (500, 100)

        # init obstacle(s)
        self.obstacles = []
        self.obstacles.append(Rectangle(500, 700, 25, 300, 0))
        self.obstacles.append(Rectangle(200, 550, 25, 200, 0))
        self.obstacles.append(Rectangle(800, 550, 25, 200, 0))

        # init rockets
        self.n_rockets = n_rockets
        self.success = 0
        self.total_success = 0
        self.rockets = []
        for i in range(n_rockets):
            self.rockets.append(
                Rocket(self.screen, self.gameSize, DNA(lifespan), lifespan, self.targetPos, self.obstacles))

        self.maxFit = 0

    # updates all rockets by moving them (i.e., advances time)
    def update(self):
        for rocket in self.rockets:
            rocket.move()

    # draws the rockets, the target, and the obstacles
    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), self.targetPos, 40, 0)
        non_alive = True

        for rocket in self.rockets:
            if rocket.alive:
                non_alive = False
            rocket.draw()
        if non_alive:
            self.rockets = self.reset()

        for obs in self.obstacles:
            pygame.draw.polygon(self.screen, (255, 255, 255), obs.get_pts())

    # resets the game
    def reset(self):
        self.generation += 1
        self.maxFit = 0
        res = []
        matingpool = self.populateMatingpool()
        self.success = 0
        for rocket in self.rockets:
            if rocket.fitness > self.maxFit:
                self.maxFit = rocket.fitness

            if rocket.arrived:
                self.success += 1
                self.total_success += 1
            r = int(random.uniform(0, len(matingpool) - 1))
            partner = matingpool[r]
            newDNA = rocket.DNA.crossover(partner)
            child = Rocket(self.screen, (1000, 1000), newDNA, self.lifespan, self.targetPos, self.obstacles)
            child.DNA.mutate()
            res.append(child)
        return res

    # run the game
    def run(self):
        while True:
            self.update()
            self.draw()
            scoretext = self.font.render(
                "Generation: %d --  last round %d rockets hit the target (%.0f perc) total hits %d" %
                (self.generation, self.success, float(self.success) / self.n_rockets * 100, self.total_success),
                1, (255, 255, 255))

            text_rect = scoretext.get_rect(center=(int(self.gameSize[0] / 2), int(self.gameSize[1] / 2)))
            self.screen.blit(scoretext, text_rect)

            scoretext2 = self.font.render("Max Fitness: %d" % (self.maxFit), 1, (255, 255, 255))

            text_rect2 = scoretext2.get_rect(center=(int(self.gameSize[0] / 2), int(self.gameSize[1] / 2) + 150))
            self.screen.blit(scoretext2, text_rect2)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.FPSCLOCK.tick(50)

    # populates the matingpool based on the fitness of rockets
    def populateMatingpool(self):
        matingpool = []
        for rocket in self.rockets:
            n = int(rocket.fitness)
            for i in range(n):
                matingpool.append(rocket)
        return matingpool

