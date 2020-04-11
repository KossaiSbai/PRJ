import csv
from src import linear_threshold as lt
import time


def run_time_spreading_nodes_test(dataset_graph,k,n):
    total_elapsed = 0
    for i in range(n):
        print("Iteration", i)
        sub = dataset_graph.return_full_subgraph(k, "o")
        start = time.time()
        influential_nodes = sub.get_influential_nodes(sub.out_degree)
        elapsed = time.time() - start
        print(elapsed)
        total_elapsed += elapsed
    return total_elapsed / float(n)


def run_influential_nodes_test(dataset_graph,k,n):
    cumulated_number_of_influential_nodes = 0
    for i in range(n):
        print("Iteration", i)
        sub = dataset_graph.return_full_subgraph(k,"i")
        influential_nodes = sub.get_influential_nodes(sub.in_degree)
        cumulated_number_of_influential_nodes += len(influential_nodes)
        print(len(influential_nodes))
    return cumulated_number_of_influential_nodes / float(n)


def run_spreading_nodes_test(dataset_graph,k,n,models_compared):
    average_spreadings = []
    for j in range(models_compared):
        average_spreadings.append([])
    for i in range(n):
        print("Iteration", i)
        sub = dataset_graph.return_full_subgraph(k,"o")
        print(len(sub.nodes))
        print(len(sub.edges))
        influential_nodes = sub.get_influential_nodes(sub.out_degree)
        random_nodes = sub.select_random_nodes(len(influential_nodes))
        spreadings = run_spreading_test(sub,influential_nodes,random_nodes,lt)
        for index,l in enumerate(average_spreadings):
            l.append(spreadings[index])
    average_spreadings = [sum(l)/float(len(l)) for l in average_spreadings]
    print(average_spreadings)
    return average_spreadings


def run_spreading_test(graph,nodes_set_1,nodes_set_2,spreading_model):
    print("Influential nodes spreading")
    _, n1 = spreading_model.cascade(graph,nodes_set_1,-1)
    print(n1)
    print("Random nodes spreading")
    _,n2= spreading_model.cascade(graph,nodes_set_2,-1)
    print(n2)
    return [n1,n2]


def write_results_to_csv_file(path, i, j, data):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        rows[i][j] = data
        writer = csv.writer(open(path, 'w'))
        writer.writerows(rows)

def compute_average_csv_file(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        data = [row[1:len(row)] for row in rows[1:len(rows)]]
        for line in data:
            line = [float(element) for element in line]
            print(line)
            print(sum(line) / float(len(line)))
        print(data)

def compute_average_spreading(path):
    result = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        data = [row[1:len(row)] for row in rows[1:len(rows)]]
        for line in data:
            print("Line",line)
            line = [element.strip('][').split(', ') for element in line]
            line = [y for x in line for y in x]
            line = [float(element) for element in line]
            print(line)
            influential_spreadings = [line[i] for i in range(0,len(line),2)]
            other_spreadings = [line[i] for i in range(1, len(line), 2)]
            print(round(sum(influential_spreadings) / float(len(influential_spreadings)),2))
            print(round(sum(other_spreadings) / float(len(other_spreadings)),2))
            print("\n")
        print("END")
        return result


def compute_average_time(path):
    result = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        data = [row[1:len(row)] for row in rows[1:len(rows)]]
        for line in data:
            print("Line",line)
            line = [float(element) for element in line]
            print(line)
            average_timing = sum(line) / float(len(line))
            print(round(average_timing,2))
        print("END")
        return result




if __name__ == "__main__":
    compute_average_spreading("CSV results files Facebook/spreading LT model comparison random vs influential OD.csv")
    compute_average_spreading("CSV results files Wikipedia/spreading LT model comparison random vs influential OD.csv")





