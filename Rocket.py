import numpy as np
import pygame
from Rectangle import Rectangle
from DNA import DNA

class Rocket(object):

    # inits a rocket, needs a reference to the screen, the dimension of the game, a set of DNA, a lifespan (of the game)
    # the position of the target, and the outline of the obstacle
    def __init__(self, screen, game_size, DNA, lifespan, target_pos, obstacles):
        rocket_lengths = 20
        rocket_widths = 4
        self.screen = screen
        self.current = 0
        self.mv_vector = np.array([0, 0])
        self.crashed = False
        self.alive = True
        self.arrived = False
        self.fitness = 0
        self.target_pos = np.array(target_pos).astype(float)
        self.target_radius = 40
        self.obstacle = obstacles
        self.game_size = game_size
        self.color = (0, 0, 255)
        self.x_init = int(game_size[0] / 2)
        self.y_init = int(game_size[1] - rocket_lengths / 2 - 1)
        self.rect = Rectangle(self.x_init, self.y_init, rocket_lengths, rocket_widths, 180)
        self.DNA = DNA

    # resets the rocket
    # not needed if Game is used
    def reset(self):
        self.alive = True
        self.arrived = False
        self.crashed = False
        self.current = 0
        self.mv_vector = np.array([0, 0])
        self.fitness = 0
        self.rect.move_to(self.x_init, self.y_init)
        self.rect.rotate_to(180)
        self.color = (0, 0, 255)

    # draws the rocket to the screen
    def draw(self):
        col = self.color
        col = (int(col[0]), int(col[1]), int(col[2]))
        pygame.draw.polygon(self.screen, col, self.rect.get_pts())

    # updates the fitness of the rocket, and moves
    def update(self):
        self.move()

    # moves the rocket if its alive, calculates the movements based on DNA, reduces fuel etc.
    def move(self):
        if (self.alive):
            self.fitness = self.calcFitness()
            # each turn, the rocket turns by 'turn' and accelerates by 'accel'
            # nasty bug-fix...
            if self.current >= len(self.DNA.genes_accel):
                self.current = 0  # ?!
            turn = self.DNA.genes_turn[self.current]
            accel = self.DNA.genes_accel[self.current]
            # turn the rocket
            self.rect.rotate_by(turn)
            self.rect.move_by(self.mv_vector[0], self.mv_vector[1])
            # accel
            self.rect.move_forwards(accel)

            # update the movement vector
            theta_rad = (90 - self.rect.theta) * np.pi / 180
            self.mv_vector = self.mv_vector + accel * np.array([np.cos(theta_rad), np.sin(theta_rad)])

            # increase the time
            self.current += 1

            # check game boundaries
            min_max = np.apply_along_axis(lambda x: [min(x), max(x)], 0, self.rect.get_pts())
            min_x = min_max[0, 0]
            max_x = min_max[1, 0]
            min_y = min_max[0, 1]
            max_y = min_max[1, 1]

            if (min_x < 0 or max_x > self.game_size[0] or min_y < 0 or max_y > self.game_size[1]):
                self.crash()

            for ob in self.obstacle:
                if (self.rect.intersect(ob)):
                    self.crash()

    # calculates the distance between two points
    @staticmethod
    def dist(pos1, pos2):
        return np.sqrt(sum((pos1 - pos2) ** 2))

    # crash the rocket
    def crash(self):
        self.alive = False
        self.crashed = True
        # self.fitness /= 10
        # self.fuel = 0
        self.color = (255, 0, 0)

    # calculates the current fitness of the rocket
    def calcFitness(self):
        rocket_pos = np.array((self.rect.x, self.rect.y)).astype(float)
        d = self.dist(rocket_pos, self.target_pos)

        fit = 1/(d+0.00001) * 100000
        #(1. / (d + 0.00001)) * 1000 + self.fuel / self.max_fuel * 100
        if d < self.target_radius:
            self.alive = False
            self.arrived = True
            self.rect.move_to(self.target_pos[0], self.target_pos[1])
            fit *= 5
        return fit