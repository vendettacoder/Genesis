# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 20:50:18 2016
@author: Rohan Kulkarni
@email : rohan.kulkarni@columbia.edu

"""

import random
from random import randint
from operator import add
import matplotlib.pyplot as plt

class Genetic_Algorithm:
    def __init__(self, population, individual_len, target, min, max):
        self.population_len = population
        self.individual_len = individual_len
        self.target = target
        self.min = min
        self.max = max
        self.population = self.initialize_population()    
        
    def initialize_individual(self):
        return [randint(self.min,self.max) for i in xrange(self.individual_len)]
        
    def initialize_population(self):
        return [self.initialize_individual() for i in xrange(self.population_len)]

    def fitness_function(self, individual):
        return abs(self.target - sum(individual))   
    
    def grade_population(self):
        summation = reduce(add, (self.fitness_function(x) for x in self.population), 0)
        return summation / self.population_len * 1.0
    
    def evolve_population(self, retain_factor = 0.2, random_select = 0.05, mutate = 0.01):      
        # Grading the current population and ordering it based on the grades        
        graded_list = [(self.fitness_function(x),x) for x in self.population]
        ordered_population = [each[1] for each in sorted(graded_list)]
        
        # Selecting the parents for the next generation based on the retain factor
        retained_population_len = int(retain_factor * self.population_len)
        parents = ordered_population[:retained_population_len]
    
        # Appending some weak performers to the parent list for genetic diversity (Avoid local minima)
        for individual in ordered_population[retained_population_len:]:
            if random_select > random.uniform(0,1):
                parents.append(individual)
        
        # Mutating some individuals in the parent list to promote diversity (Avoid local minima)
        for individual in parents:
            if mutate >= random.uniform(0,1):
                index = randint(0,len(individual)-1)
                individual[index] = randint(min(individual),max(individual))
        
        # Breeding parents to produce the next generation
        children = list()
        while len(children) < self.population_len - len(parents):
            male = randint(0,len(parents)-1)
            female = randint(0,len(parents)-1)
            if male != female:
                male , female = parents[male] , parents[female]
                half = len(male)/2 
                child = male[:half] + female[half:]
                children.append(child)
        parents.extend(children)
        self.population = parents
            
            
def main():
    population = 100
    individual_len = 10 
    target = 200 
    min = 0
    max = 100
    obj = Genetic_Algorithm(population, individual_len, target, min, max)
    max_iterations = 100
    history = [obj.grade_population()]

    solution = list()
    for i in xrange(max_iterations-1):
        obj.evolve_population()
        temp = obj.grade_population()
        history.append(temp)
        if not temp:
            solution = obj.population[0]
    if not solution:
        solution = obj.population[0]
        
    print "One possible closest solution for these iterations is : " , solution
    
    x = range(max_iterations)
    plt.plot(x,history,'r')
    plt.xlabel('Iteration')
    plt.ylabel('Overall population fitness')
    plt.show()
    
if __name__=='__main__':
    main()

