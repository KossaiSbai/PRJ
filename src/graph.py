from operator import itemgetter
from random import randint
import math
import random


class Graph:
    """An example docstring for a class definition."""
    def __init__(self, path="", al=None):
        """
        Blah blah blah.
        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.
        """
        self.adjacency_list = {}
        self.nodes = []
        if path != "":
            self.process_tgf_file(path) if file_type(path) == "tgf" else self.process_txt_file(path)
        else:
            self.adjacency_list = al
            self.nodes = self.get_vertices()
        self.edges = self.get_edges()
        self.most_connected_node = None
        self.degree_centralities = {}

    def get_edges(self):
        """
        Blah blah blah.
        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.
        """
        self.edges = []
        for node,neighbours in self.adjacency_list.items():
            node_edges = [(node,neighbour) for neighbour in neighbours]
            self.edges.extend(node_edges)
        return self.edges

    def get_vertices(self):
        """
        Blah blah blah.
        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.
        """
        return list(self.adjacency_list.keys())

    def get_adjacency_list(self):
        return self.adjacency_list

    def build_adjacency_list(self, lines):
        for x in lines:
            end_nodes = x.split(" ")
            from_node = end_nodes[0]
            to_node = end_nodes[1]
            if from_node == to_node:
                continue
            if from_node not in self.adjacency_list.keys():
                self.adjacency_list[from_node] = [to_node]
            else:
                self.adjacency_list[from_node].append(to_node)

            if to_node not in self.adjacency_list.keys():
                self.adjacency_list[to_node] = []

        return self.adjacency_list

    def process_tgf_file(self, path):
        line_list = [' '.join(line.split()) for line in open(path, "r")]
        hashtag_index = line_list.index("#")
        nodes_part = line_list[:hashtag_index]
        edges_part = line_list[hashtag_index+1:]
        self.adjacency_list = self.build_adjacency_list(edges_part)
        self.nodes = [nodes_part[i].split(" ")[0] for i in range(len(nodes_part))]

    def process_txt_file(self, path):
        line_list = [' '.join(line.split()) for line in open(path, "r")]
        self.adjacency_list = self.build_adjacency_list(line_list)
        self.nodes = self.get_vertices()

    def in_degree(self, vertex):
        in_neighbours = [node for node in self.nodes if vertex in self.adjacency_list[node]]
        return len(in_neighbours)

    def out_degree(self, vertex):
        return len(self.adjacency_list[vertex])

    def vertices_with_degree(self, degree_method, vertices):
        degrees_tuples = [(vertex, degree_method(vertex)) for vertex in vertices]
        return degrees_tuples

    def sort_vertices_by_degree(self, degree_method, vertices):
        degrees_tuples = self.vertices_with_degree(degree_method, vertices)
        degrees_sorted = sorted(degrees_tuples, key=itemgetter(1), reverse=True)
        return degrees_sorted

    def vertices_with_in_degree(self, vertices):
        return self.vertices_with_degree(self.in_degree, vertices)

    def sort_vertices_by_in_degree(self, vertices):
        return self.sort_vertices_by_degree(self.in_degree, vertices)

    def vertices_with_out_degree(self, vertices):
        return self.vertices_with_degree(self.out_degree, vertices)

    def sort_vertices_by_out_degree(self, vertices):
        return self.sort_vertices_by_degree(self.out_degree, vertices)

    def select_k_most_vertices(self,degree_method,k):
        degrees_sorted = self.sort_vertices_by_degree(degree_method,self.nodes)
        return [degree_tuple[0] for degree_tuple in degrees_sorted][0:k]

    def neighbourhood(self, vertex):
        nodes = self.adjacency_list.keys()
        neighbours = [node for node in nodes if node in self.adjacency_list[vertex] or vertex in self.adjacency_list[node]]
        return neighbours

    def number_of_edges_within_neighbourhood(self, neighbourhood):
        neighbourhood_edges = 0
        for neighbour in neighbourhood:
            neighbourhood_edges += len(list(set(neighbourhood) & set(self.adjacency_list[neighbour])))
        return neighbourhood_edges

    def local_clustering_coefficient(self, vertex):
        neighbourhood = self.neighbourhood(vertex)
        if len(neighbourhood) > 1:
            return self.number_of_edges_within_neighbourhood(neighbourhood) / (len(neighbourhood) * (len(neighbourhood)-1))
        return 0.0

    def node_level_centrality(self, degree_method, vertex):
        connected_graph_neighbours = self.neighbourhood(vertex)
        connected_graph_neighbours.append(vertex)
        degrees = self.sort_vertices_by_degree(degree_method,connected_graph_neighbours)
        most_connections = degrees[0][1]
        degree_centrality = sum([most_connections - degree[1] for degree in degrees])
        return degree_centrality

    def mcn(self, degree_method):
        most_connected_node = self.sort_vertices_by_degree(degree_method, self.get_vertices())[0][1]
        return most_connected_node

    def degree_centrality(self, degree_method, vertex):
        node_level_centrality = self.node_level_centrality(degree_method, vertex)
        if node_level_centrality != 0:
            return (self.most_connected_node- degree_method(vertex)) / node_level_centrality
        else:
            return self.most_connected_node - degree_method(vertex)

    def enhanced_degree_centrality(self, degree_method, vertex):
        degree_centrality = self.degree_centrality(degree_method,vertex)
        lcc = self.local_clustering_coefficient(vertex)
        self.degree_centralities[vertex] = float(degree_centrality)
        return abs(degree_centrality*lcc)

    def successors(self, vertex):
        successors = self.adjacency_list[vertex]
        return successors

    def predecessors(self, vertices, vertex):
        predecessors = [v for v in vertices if vertex in self.adjacency_list[v]]
        return predecessors

    def average_enhanced_degree_centrality(self, edcs):
        return sum([x[1] for x in edcs])/float(len(edcs))

    def sort_by_special_degree_centrality_measures(self, metric,submetric,vertices):
        degrees_tuples = [(vertex, metric(submetric, vertex)) for vertex in vertices]
        degrees_sorted = sorted(degrees_tuples, key=itemgetter(1), reverse=True)
        return degrees_sorted

    def sort_nodes_by_edc(self,degree_method,vertices):
        return self.sort_by_special_degree_centrality_measures(self.enhanced_degree_centrality,degree_method,vertices)

    def sort_nodes_by_degree_centrality(self, degree_method,vertices):
        return self.sort_by_special_degree_centrality_measures(self.degree_centrality,degree_method,vertices)

    def filter_out_nodes_edc_threshold(self,nodes_tuples,threshold):
        final_nodes = [x[0] for x in nodes_tuples if self.degree_centralities[x[0]] >= threshold]
        print(final_nodes)
        return final_nodes

    def active_nodes(self, nodes_list):
        quarter = math.ceil(len(nodes_list)/4)
        print(quarter)
        return nodes_list[0:quarter]

    def get_influential_nodes(self, degree_method):
        graph_nodes = self.nodes
        if self.most_connected_node is None:
            self.most_connected_node = self.mcn(degree_method)
        edcs = self.sort_nodes_by_edc(degree_method,graph_nodes)
        average_edc = self.average_enhanced_degree_centrality(edcs)
        fn = self.filter_out_nodes_edc_threshold(edcs,average_edc)
        return self.active_nodes(fn)

    def select_random_nodes(self,k):
        vertices = self.get_vertices()
        selected_nodes = random.sample(vertices,k=k)
        return selected_nodes

    def get_subgraph(self, nodes):
        new_al = {}
        for node in nodes:
            out_nodes = [out_node for out_node in self.adjacency_list[node] if out_node in nodes]
            new_al[node] = out_nodes
        return new_al

    def return_full_subgraph(self, number_of_nodes,degree_method_string):
        new_al = self.get_subgraph(self.select_random_nodes(number_of_nodes))
        sub = Graph("", new_al)
        degree_method = sub.in_degree if degree_method_string == "i" else sub.out_degree
        sub.most_connected_node = sub.mcn(degree_method)
        return sub

    def return_full_subgraph2(self, nodes):
        new_al = self.get_subgraph(nodes)
        sss = Graph("", new_al)
        return sss


def generate_random_graph():
    entries = []
    for i in range(2000):
        a = randint(1,500)
        b = randint(1,500)
        while a == b or (a,b) in entries:
            a = randint(1,500)
            b = randint(1,500)
        entries.append((a,b))
        print(a,b)


def file_type(filename):
    file = list(filename)
    dot_index = file.index(".")
    file_type = "".join(filename[dot_index+1:])
    return file_type


def store_influential_nodes(path, nodes):
    with open(path, 'w') as output_file:
        for index, node in enumerate(nodes):
            output_file.write(node)
            if index != len(nodes) - 1:
                output_file.write("\n")


def write_graph_txt_file(path,g):
    with open(path, 'w') as output_file:
        edges = g.edges
        for index, edge in enumerate(edges):
            output_file.write(edge[0] + " " + edge[1])
            if index != len(edges) - 1:
                output_file.write("\n")


if __name__ == "__main__":
    g = Graph("wiki-Vote.txt")
    sub = g.return_full_subgraph(3500,"o")
    sub.get_influential_nodes(sub.out_degree)




