import numpy as np

"""
Bin Packing Problem generator
Contains BinPacking Problem class
"""


class BinPackingProblem:
    def __init__(self, b, n, min, max, bpp2=False):
        """
        Constuctor for BinPackingProblem class
        :param b: number of bins
        :param n: number of items
        :param min: min weight of an item in the dataset
        :param max: max weight of an item in the dataset
        :param bpp2: If value is true, executes BPP2
        """
        self.__n = n
        self.__num_bins = b
        self.__min = min
        self.__max = max
        if bpp2:
            self._weights = self.__create_data2()
        else:
            self._weights = self.__create_data1()

        self._bins = [[] for _ in range(b)]

    # Private helper function to create dataset for BPP1
    def __create_data1(self):
        data = np.random.randint(self.__min, self.__max, self.__n)
        return data

    # Private helper function to create dataset for BPP2
    def __create_data2(self):
        w = []
        for b in range(self.__n):
            i = np.random.randint(self.__min, self.__max)
            j = np.random.randint(self.__min, self.__max)
            c = (i * j) / 2
            w.append(c)
        c = np.array(w)
        return c

    def clear_bins(self):
        self._bins = [[] for _ in range(self.__num_bins)]

    def path_to_bin(self, path):
        """
        Executes created path, inserting items in the bins
        :param path: constructed path
        """
        for i in range(len(path)):
            self._bins[path[i]].append(self._weights[i])



    """
    Getters for BPP
    """

    def get_bins(self):
        return self._bins

    def get_weights(self):
        return self._weights

    def get_num_bins(self):
        return self.__num_bins

    def calculate_fitness(self):
        """
        Calculates fitness of bins
        :return: fitness
        """
        sum_bins = []
        for i in self._bins:
            sum_bins.append(sum(i))
        difference = max(sum_bins) - min(sum_bins)
        return difference

    def pheromone_matrix(self):
        """
        Creates a pheromone_matrix
        :return: pheromone matrix
        """
        len_bins = len(self._bins)
        len_items = len(self._weights)
        mat = np.random.rand(len_bins, len_items)
        return mat
