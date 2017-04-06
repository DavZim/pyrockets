import random

class DNA(object):

    # inits a new strand of DNA
    def __init__(self, lifespan, geneturn=[], geneaccel=[]):
        self.lifespan = lifespan
        self.genes_turn = geneturn
        self.genes_accel = geneaccel
        self.turn_mean = 0
        self.turn_sd = 10
        self.accel_min = 0
        self.accel_max = 0.25

        # if the given DNA is not the same length as the lifespan, create new
        if len(geneturn) == 0:
            self.genes_turn = []
            self.genes_accel = []
            for i in range(lifespan):
                self.genes_turn.append(random.gauss(self.turn_mean, self.turn_sd))
                self.genes_accel.append(random.uniform(self.accel_min, self.accel_max))

    # mutate the DNA
    def mutate(self):
        for i in range(self.lifespan):
            if random.uniform(0, 1) < 0.01:
                self.genes_turn[i] = random.gauss(self.turn_mean, self.turn_sd)
            if random.uniform(0, 1) < 0.01:
                self.genes_accel[i] = random.uniform(self.accel_min, self.accel_max)

    # crossover between DNA and partner DNA
    def crossover(self, partner):
        newgenes_turn = []
        newgenes_accel = []

        # currently the child's DNA is sampled per gene
        v = random.choice(range(len(self.genes_accel)))

        newgenes_turn.extend(partner.DNA.genes_turn[:v])
        newgenes_accel.extend(partner.DNA.genes_accel[:v])
        newgenes_turn.extend(self.genes_turn[v:])
        newgenes_accel.extend(self.genes_accel[v:])

        # create the new instance of DNA
        dna = DNA(self.lifespan, newgenes_turn, newgenes_accel)
        return dna