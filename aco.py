import time
import numpy as np

"""
Ant Colony Optimization module
For Bin Packing Problem
Contatins class Colony

"""


class ACO:
    """
    Class ACO
    Performs n iterations with b ants and returns n fitness evaluations
    """

    def __init__(self, BinPacketProblem, amountOfAnts, evaporation_rate, maxFitnesses=10000):
        """
        Constructor for ACO class
        :param BinPacketProblem: instance object of BinPacketProblem class
        :param amountOfAnts: int number for amount of ants per iteration
        :param evaporation_rate: evaporation_rate for pheromone matrix
        :param maxFitnesses: number of fitness evaluations to find
        """
        self.__bpp = BinPacketProblem
        self.__matrix = self.__bpp.pheromone_matrix()
        self.__transpose_matrix = self.__matrix.T
        self.__ants = amountOfAnts
        self.__e = evaporation_rate
        self.__maxFit = maxFitnesses
        self.__list_of_paths = []
        self.__fitness_evaluations = []
        self.exec_time = 0

    def __traverse_path(self, bins):
        """
        Function to create one path
        :param bins: instance of the bins array from BPP
        :return: path
        """
        inner_path = []
        for column in self.__transpose_matrix:
            probabilities = []
            sum_column = sum(column)
            for i in column:
                probability = i / sum_column
                probabilities.append(probability)
            choice = np.random.choice(np.arange(0, bins), p=probabilities)
            inner_path.append(choice)
        return inner_path

    def __update(self, fitness, path):
        """
        Update rule for ACO
        :param fitness: Fitness of the evaluation
        :param path: path of the given fitness
        :return: updates pheromone matrix
        """
        b = self.__transpose_matrix
        for i in range(len(path)):
            b[i][path[i]] = 100 / fitness

    def __evaporate(self, paths, rate):
        """
        Evaporation function for ACO
        :param paths: created path
        :param rate: evaporation rate
        :return: updates pheromone matrix
        """
        b = self.__transpose_matrix
        for c in range(len(paths)):
            for i in range(len(paths[c])):
                b[i][paths[c][i]] *= rate

    def iterate(self):
        """
        Iterates path construction until maximum value of
        fitness iteration has been reached
        """
        num_iter = 0
        start = time.time()
        print("ACO started")
        while len(self.__fitness_evaluations) != self.__maxFit:
            paths = {}
            for i in range(self.__ants):
                paths[i] = self.__traverse_path(self.__bpp.get_num_bins())
                self.__bpp.path_to_bin(paths[i])
                fitness = self.__bpp.calculate_fitness()
                self.__update(fitness, paths[i])
                self.__fitness_evaluations.append(fitness)
            self.__evaporate(paths, self.__e)
            self.__bpp.clear_bins()
            self.__list_of_paths.append(paths)
            num_iter += 1
            if len(self.__fitness_evaluations) % 1000 == 0:
                print("ACO with " + str(self.__ants) + " ants and " + str(self.__e) + " evaporation rate, has: " +
                      str(len(self.__fitness_evaluations)) + " fitness evaluations")
        end = time.time()
        self.exec_time = end - start
        print("ACO is done, with " + str(self.get_min_fitness()[0]) + " as best evaluation")
        print("Mean of fitness evaluations: " + str(self.get_mean()))
        print("Standard Deviation of fitness evaluations: " + str(self.get_standard_dev()))
        print("Execution time: " + str(self.exec_time))

    """
        Statistical functions for BPP
    """

    def get_mean(self):
        return np.mean(self.__fitness_evaluations)

    def get_standard_dev(self):
        return np.std(self.__fitness_evaluations)

    """
    Getters for ACO class
    """

    def get_paths(self):
        return self.__list_of_paths

    def get_exec_time(self):
        return self.exec_time

    def get_fitness_evaluations(self):
        return self.__fitness_evaluations

    def get_min_fitness(self):
        best = min(self.__fitness_evaluations)
        index_best = self.__fitness_evaluations.index(best)
        return best, index_best

    def get_max_fitness(self):
        return max(self.__fitness_evaluations)

    def get_best_path(self):
        fit, index_fit = self.get_min_fitness()
        best_fit_iter = (index_fit - (index_fit % self.__ants)) / self.__ants
        bestFitPath = self.__list_of_paths[int(best_fit_iter)][int(index_fit % self.__ants)]
        return bestFitPath

    def get_matrix(self):
        return self.__matrix
