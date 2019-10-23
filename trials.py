
from bpp import BinPackingProblem
from aco import ACO


def trial(trials, bins, items, ants, evaporation_rate, bpp2):
    """
    Trials function. Performs n ACO trials
    :param trials: amount of trials
    :param bins: amount of bins
    :param items: amount of items
    :param ants: amount of ants
    :return: a list with minimal fitness, index of the best path,
    best path, bins and execution time.
    """
    overall_output = []
    for i in range(trials):
        b = BinPackingProblem(bins, items, 1, items, bpp2)
        aco = ACO(b, ants, evaporation_rate)
        aco.iterate()
        min_fit, min_index = aco.get_min_fitness()
        best_path = aco.get_best_path()
        b.path_to_bin(best_path)
        output_trial = [min_fit, min_index, best_path, b.get_bins(), aco.get_exec_time()]
        overall_output.append(output_trial)
    return overall_output


if __name__ == "__main__":

    bpp1 = [trial(5, 10, 200, 100, 0.90, False), trial(5, 10, 200, 100, 0.40, False),
            trial(5, 10, 200, 10, 0.90, False), trial(5, 10, 200, 10, 0.40, False)]
    bpp2 = [trial(5, 50, 200, 100, 0.90,True),trial(5, 50, 200, 100, 0.40, True),
            trial(5, 50, 200, 10, 0.90, True), trial(5, 50, 200, 10, 0.40, True)]

    fitnesses_bpp2 = []
    for i in range(len(bpp2)):
        for x in bpp2[i]:
            fitnesses_bpp2.append(x[0])

    fitnesses_bpp1 = []
    for i in range(len(bpp1)):
        for x in bpp1[i]:
            fitnesses_bpp1.append(x[0])

    print(fitnesses_bpp1)
    print(min(fitnesses_bpp1))
    print(fitnesses_bpp2)
    print(min(fitnesses_bpp2))
