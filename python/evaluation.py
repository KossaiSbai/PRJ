import csv
from python.linear_threshold import LinearThresholdModel
from python.independent_cascade import IndependentCascadeModel
from python.graph import Graph
import time
from typing import List,Any


def run_time_spreading_nodes_test(dataset_graph: Graph, k: int, n: int) -> float:
    """ Computes the average time taken by the IM algorithm to compute the influential nodes.

    Parameters
    ----------
    dataset_graph :  Graph
        graph on which the test is carried out.

    k :  int
        size of subgraph.

    n :  int
        number of iterations of the test.

    Returns
    -------
    float
        average running time.
    """
    total_elapsed = 0
    for i in range(n):
        print("Iteration", i)
        sub = dataset_graph.build_subgraph(k, "o")
        start = time.time()
        influential_nodes = sub.get_influential_nodes(sub.out_degree)
        elapsed = time.time() - start
        print(elapsed)
        total_elapsed += elapsed
    return total_elapsed / float(n)


def run_influential_nodes_test(dataset_graph: Graph, k: int, n: int) -> float:
    """ Computes the average number of influential nodes returned by the IM algorithm.

    Parameters
    ----------
    dataset_graph :  Graph
        graph on which the test is carried out.

    k :  int
        size of subgraph

    n :  int
        number of iterations of the test.

    Returns
    -------
    float
        average running time.
    """
    cumulated_number_of_influential_nodes = 0
    for i in range(n):
        print("Iteration", i)
        sub = dataset_graph.build_subgraph(k, "i")
        influential_nodes = sub.get_influential_nodes(sub.in_degree)
        cumulated_number_of_influential_nodes += len(influential_nodes)
        print(len(influential_nodes))
    return cumulated_number_of_influential_nodes / float(n)


def run_spreading_nodes_test(dataset_graph: Graph, k: int, n: int, methods_compared: int) -> List[float]:
    """ Computes the average number of influenced nodes using two methods (influential vs random for example) after diffusion by a given spreading model.

    Parameters
    ----------
    dataset_graph :  Graph
        graph on which the test is carried out.

    k :  int
        size of subgraph

    n :  int
        number of iterations of the test.

    methods_compared :  int
        number of methods that are compared.

    Returns
    -------
    List[float]
        list of average spreading influence values.
    """
    average_spreadings = []
    # Each sublist of average_spreadings stores the spreadings obtained via a given method.
    # Hence, there will be as many sublists as compared methods.
    for j in range(methods_compared):
        average_spreadings.append([])
    for i in range(n):
        sub = dataset_graph.build_subgraph(k, "o")
        influential_nodes = sub.get_influential_nodes(sub.out_degree)
        other_nodes = sub.select_random_nodes(len(influential_nodes))
        spreadings = compute_spreading_influence_values(sub, influential_nodes, other_nodes, LinearThresholdModel)
        # Appends the spreading obtained by each method in its associated sublist in average_spreadings
        for index,l in enumerate(average_spreadings):
            l.append(spreadings[index])
    average_spreadings = [sum(l)/float(len(l)) for l in average_spreadings]
    print(average_spreadings)
    return average_spreadings


def compute_spreading_influence_values(dataset_graph: Graph, nodes_set_1: List[str], nodes_set_2: List[str], spreading_model: Any) -> List[float]:
    """ Computes the total number of influenced nodes after diffusion by a given spreading model. Two sets of nodes `nodes_set_1` and `nodes_set_2` are used as seed nodes.

    Parameters
    ----------
    dataset_graph :  Graph
        graph on which the test is carried out.

    nodes_set_1 :  List[str]
        first set of nodes (influential nodes in our case).

    nodes_set_2 :  List[str]
        second set of nodes (random nodes, in-degree nodes etc).

    spreading_model : Any
        spreading model used: either IC or LT.

    Returns
    -------
    List[float]
        list of average spreading influence values.
    """
    print("Influential nodes spreading")
    sm1 = spreading_model(dataset_graph, nodes_set_1, 0.2)
    sm2 = spreading_model(dataset_graph, nodes_set_2, 0.2)
    n1 = sm1.get_total_number_of_influenced_nodes()
    print(n1)
    print("Other nodes spreading")
    n2 = sm2.get_total_number_of_influenced_nodes()
    print(n2)
    return [n1,n2]


def write_results_to_csv_file(path: str, i: int, j: int, data: Any) -> None:
    """ Writes `data` in the given csv file.

    Parameters
    ----------
    path :  str
        path of the csv file.

    i :  int
        index of the row of the csv file to write to.

    j :  int
        index of the cell within the row of the csv file to write to.

    data : Any
        data to write in the csv file.
    """
    with open(path, 'r') as f:
        # Extracts the rows, modifies them and overwrites the current content of the CSV file.
        reader = csv.reader(f)
        rows = list(reader)
        rows[i][j] = data
        writer = csv.writer(open(path, 'w'))
        writer.writerows(rows)


if __name__ == "__main__":
    g = Graph("../wiki-Vote.txt")
    s = g.build_subgraph(1000, "o")
    seeds = s.get_influential_nodes(s.out_degree)
    print(len(seeds))
    random_nodes = s.select_vertices_with_k_biggest_degree_values(s.out_degree,len(seeds))
    compute_spreading_influence_values(s,seeds,random_nodes,IndependentCascadeModel)





