#import matplotlib.pyplot as plt
import numpy as np
from io_helper import read_tsp, normalize
from sys import argv
import math, random
from operator import attrgetter
from time import time

citySize = 0
cities = []

def dis(a, b):
    x = (a[1] - b[1]) * (a[1] - b[1])
    y = (a[2] - b[2]) * (a[2] - b[2])
    return math.sqrt(x + y)

def getPathCost(path):
    tot = 0
    for i in range(citySize - 1):
        tot += dis(path[i], path[i + 1])
    tot += dis(path[citySize - 1], path[0])
    return tot

class Particle:
    def __init__(self, solution, cost):
        # solution means position aka the sequence of TPS
        self.solution = solution
        self.pbest = solution
        self.cost = cost
        self.pbestCost = cost
        self.velocity = []
    def setSolution(self, solution):
        self.solution = solution
    def getSolution(self):
        return self.solution
    def setPbest(self, pbest):
        self.pbest = pbest
    def getPbest(self):
        return self.pbest
    def setCost(self, cost):
        self.cost = cost
    def getCost(self):
        return self.cost
    def setPbestCost(self, cost):
        self.pbestCost = cost
    def getPbestCost(self):
        return self.pbestCost
    def setVolecity(self, velocity):
        self.velocity = velocity
    def getVelocity(self):
        return self.velocity
    def clear(self):
        del self.velocity[:]

class PSO:
    def __init__(self, iterations, swarmSize, alpha, beta):
        self.iterations = iterations
        self.swarmSize = swarmSize
        self.swarm = []
        self.alpha = alpha
        self.beta = beta
        global cities
        def getRandomSwarm(swarmSize):
            random_path = []
            cnt = 0
            while cnt < swarmSize:
                tmp = list(cities)
                random.shuffle(tmp)
                if tmp not in random_path:
                    random_path.append(list(tmp))
                    cnt = cnt + 1
            return random_path

        res = getRandomSwarm(self.swarmSize)
        for path in res:
            particle = Particle(solution=path, cost=getPathCost(path))
            self.swarm.append(particle)

        # print(len(self.swarm))
    def run(self):
        last = 0
        cnt = 0
        for _ in range(self.iterations):
            self.gbest = min(self.swarm, key=attrgetter('pbestCost'))
            if(last != 0):
                if(self.gbest.getPbestCost() == last):
                    cnt = cnt + 1
                else:
                    cnt = 0
            last = self.gbest.getPbestCost()
            if(cnt >= 50):
                break
            print('Iteration ', _, ': ', self.gbest.getPbestCost())
            for particle in self.swarm:
                # swapSequence = list(particle.getVelocity())
                swapSequence = []
                particle.clear()
                # print(len(swapSequence))
                gbestSolution = self.gbest.getPbest()
                pbestSolution = particle.getPbest()
                currentSolution = particle.getSolution()
                for i in range(citySize):
                    swapOperator = (i, pbestSolution.index(currentSolution[i]), self.alpha)
                    swapSequence.append(swapOperator)
                for i in range(citySize):
                    swapOperator = (i, gbestSolution.index(currentSolution[i]), self.beta)
                    swapSequence.append(swapOperator)
                particle.setVolecity(swapSequence)

                # Update Solution
                for SO in swapSequence:
                    if random.random() <= SO[2]:
                        currentSolution[SO[0]], currentSolution[SO[1]] = currentSolution[SO[1]], currentSolution[SO[0]]
                particle.setSolution(currentSolution)
                cost = getPathCost(currentSolution)
                particle.setCost(cost)
                if cost < particle.getPbestCost():
                    particle.setPbest(currentSolution)
                    particle.setPbestCost(cost)





def init():
    if len(argv) != 2:
        print("Correct use: python src/main.py <filename>.tsp")
        return -1
    filepath = 'assets/' + argv[1]
    df = read_tsp(filepath)
    global cities, citySize
    cities = df.values.tolist()
    citySize = len(cities)
    # print(cities)


def main():
    init()
    pso = PSO(iterations=200, swarmSize=20, alpha=0.40, beta=0.20)
    start = time()
    pso.run()
    stop = time()
    print("Elapsed time: ", str(stop-start))


if __name__=='__main__':
    main()
