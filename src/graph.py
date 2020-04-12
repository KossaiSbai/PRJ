from operator import itemgetter
from random import randint
import math
import random
import src.linear_threshold as lt
from typing import List,Callable,Tuple,Dict


class Graph:

    """Conceptual class representing a graph data structure

    Parameters
    ----------
    path : str, optional
        Path of the txt file. Defaults to "".

    al : dict, optional
        Adjacency list. Defaults to None.
    """

    def __init__(self, path="", al=None):
        """
        Constructor method.
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

    def get_edges(self) -> List[Tuple[str,str]]:
        """Extracts and returns the edges of `self`.

        Returns
        -------
        List[Tuple[str,str]]
            A list of tuples where each tuple (`a`, `b`) is an edge between `a` and `b`.
        """

        self.edges = []
        for node,neighbours in self.adjacency_list.items():
            node_edges = [(node,neighbour) for neighbour in neighbours]
            self.edges.extend(node_edges)
        return self.edges

    def get_vertices(self) -> List[str]:
        """Extracts and returns the vertices of `self`.

        Returns
        -------
        List[str]
            A list of strings where each string `v`, is a node `v` of the graph.
        """

        return list(self.adjacency_list.keys())

    def get_adjacency_list(self) -> Dict[str,List[str]]:
        """Extracts and returns the adjacency list of `self`.

        Returns
        -------
        Dict[str,List[str]]
            A dictionary which entries (`v`, `e`) associate each node `v` to its outgoing nodes `e`.
        """

        return self.adjacency_list

    def build_adjacency_list(self, lines: List[str]) -> Dict[str,List[str]]:
        """ Builds the adjacency list of `self` from the content of a file (txt or tgf).

        Parameters
        ----------
        lines :  List[str]
            List of strings (`a`, `b`) denoting an edge between `a` and `b`.

        Returns
        -------
        Dict[str,List[str]]
            The adjacency list of `self`.
        """
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

    def process_tgf_file(self, path: str) -> None:
        """ Builds and stores the graph from a tgf file.

        Parameters
        ----------
        path : str
            Path of the tgf file.
        """
        line_list = [' '.join(line.split()) for line in open(path, "r")]
        hashtag_index = line_list.index("#")
        nodes_part = line_list[:hashtag_index]
        edges_part = line_list[hashtag_index+1:]
        self.adjacency_list = self.build_adjacency_list(edges_part)
        self.nodes = [nodes_part[i].split(" ")[0] for i in range(len(nodes_part))]

    def process_txt_file(self, path: str) -> None:
        """  Builds and stores the graph from a txt file.

        Parameters
        ----------
        path : str
            Path of the txt file.
        """
        line_list = [' '.join(line.split()) for line in open(path, "r")]
        self.adjacency_list = self.build_adjacency_list(line_list)
        self.nodes = self.get_vertices()

    def in_degree(self, vertex: str) -> int:
        """ Calculates the in-degree of the `vertex`.

        Parameters
        ----------
        vertex : str
            Vertex for which the in-degree is calculated.

        Returns
        -------
        int
            The in-degree of the vertex.
        """
        in_neighbours = [node for node in self.nodes if vertex in self.adjacency_list[node]]
        return len(in_neighbours)

    def out_degree(self, vertex: str) -> int:
        """ Calculates the out-degree of the `vertex`.

        Parameters
        ----------
        vertex : str
            Vertex for which the out-degree is calculated.

        Returns
        -------
        int
            The out-degree of the vertex.
        """
        return len(self.adjacency_list[vertex])

    def vertices_with_degree(self, degree_method: Callable[[str], int], vertices: List[str]) -> List[Tuple[str,int]]:
        """ Computes and stores the degree values for each node, using the given degree metric.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        vertices : List[str]
            List of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        degrees_tuples = [(vertex, degree_method(vertex)) for vertex in vertices]
        return degrees_tuples

    def sort_vertices_by_degree(self, degree_method: Callable[[str], int], vertices: List[str]) -> List[Tuple[str, int]]:
        """Sorts the nodes by degree value.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        vertices : List[str]
            List of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        degrees_tuples = self.vertices_with_degree(degree_method, vertices)
        degrees_sorted = sorted(degrees_tuples, key=itemgetter(1), reverse=True)
        return degrees_sorted

    def vertices_with_in_degree(self, vertices: List[str]) -> List[Tuple[str,int]]:
        """ Computes and stores the in-degree values for each node.

        Parameters
        ----------
        vertices : List[str]
            List of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        return self.vertices_with_degree(self.in_degree, vertices)

    def sort_vertices_by_in_degree(self, vertices: List[str]) -> List[Tuple[str,int]]:

        """ Sorts the nodes by in-degree value.

        Parameters
        ----------
        vertices : List[str]
            List of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its in-degree value.
        """
        return self.sort_vertices_by_degree(self.in_degree, vertices)

    def vertices_with_out_degree(self, vertices: List[str]) -> List[Tuple[str,int]]:
        """ Computes and stores the out-degree values for each node.

        Parameters
        ----------
        vertices : List[str]
            List of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        return self.vertices_with_degree(self.out_degree, vertices)

    def sort_vertices_by_out_degree(self, vertices: List[str]) -> List[Tuple[str,int]]:
        """ Sorts the nodes by out-degree value.

        Parameters
        ----------
        vertices : List[str]
            List of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its out-degree value.
        """
        return self.sort_vertices_by_degree(self.out_degree, vertices)

    def select_k_most_vertices(self, degree_method:  Callable[[str], int], k: int) -> List[str]:
        """ Retrieve case ID from file name.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        k : int
           Number of vertices to be selected.

        Returns
        -------
         List[str]
            List of selected vertices.
        """
        degrees_sorted = self.sort_vertices_by_degree(degree_method, self.nodes)
        return [degree_tuple[0] for degree_tuple in degrees_sorted][0:k]

    def neighbourhood(self, vertex: str) -> List[str]:
        """ Determines the neighbourhood of `vertex`, which are the nodes connected to `vertex` by either an outgoing or incoming edge.

        Parameters
        ----------
        vertex : str
            Vertex which neighbourhood is determined.

        Returns
        -------
        List[str]
            A list of nodes corresponding to the neighbourhood of `vertex`.
        """
        nodes = self.adjacency_list.keys()
        neighbours = [node for node in nodes if node in self.adjacency_list[vertex] or vertex in self.adjacency_list[node]]
        return neighbours

    def number_of_edges_within_neighbourhood(self, neighbourhood: List[str]) -> int:
        """ Determines the number of edges linking nodes in a given neighbourhood.

        Parameters
        ----------
        neighbourhood : List[str]
            List of neighbours.

        Returns
        -------
        int
            Number of edges within neighbourhood.
        """
        neighbourhood_edges = 0
        for neighbour in neighbourhood:
            neighbourhood_edges += len(list(set(neighbourhood) & set(self.adjacency_list[neighbour])))
        return neighbourhood_edges

    def local_clustering_coefficient(self, vertex: str) -> float:
        """ Computes the local clustering coefficient of `vertex`, `LCC(vertex)`.

        Parameters
        ----------
        vertex : str
            Vertex for which the local clustering coefficient is computed.

        Returns
        -------
        float
            `LCC(vertex)`
        """
        neighbourhood = self.neighbourhood(vertex)
        if len(neighbourhood) > 1:
            return self.number_of_edges_within_neighbourhood(neighbourhood) / (len(neighbourhood) * (len(neighbourhood)-1))
        return 0.0

    def node_level_centrality(self, degree_method: Callable[[str], int], vertex: str) -> float:
        """ Computes the node level centrality of `vertex`, `NLC(vertex)`.

        Parameters
        ----------
        vertex : str
            Vertex for which the  node level centrality is computed.
        
        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.    

        Returns
        -------
        float
            `NLC(vertex)`
        """
        connected_graph_neighbours = self.neighbourhood(vertex)
        connected_graph_neighbours.append(vertex)
        degrees = self.sort_vertices_by_degree(degree_method,connected_graph_neighbours)
        most_connections = degrees[0][1]
        degree_centrality = sum([most_connections - degree[1] for degree in degrees])
        return degree_centrality

    def mcn(self, degree_method: Callable[[str], int]) -> int:
        """ Iterates through the nodes in `self` and retrieves the biggest degree value.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.   

        Returns
        -------
        int
            Biggest degree value in the given graph.
        """
        most_connected_node = self.sort_vertices_by_degree(degree_method, self.get_vertices())[0][1]
        return most_connected_node

    def degree_centrality(self, degree_method: Callable[[str], int], vertex: str) -> float:
        """ Computes the degree centrality of `vertex`, `DC(vertex)`.

        Parameters
        ----------
        vertex : str
            Vertex for which the  degree centrality is computed.

        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        Returns
        -------
        float
            `DC(vertex)`
        """
        node_level_centrality = self.node_level_centrality(degree_method, vertex)
        if node_level_centrality != 0:
            return (self.most_connected_node- degree_method(vertex)) / node_level_centrality
        else:
            return self.most_connected_node - degree_method(vertex)

    def enhanced_degree_centrality(self, degree_method: Callable[[str], int], vertex: str) -> float:
        """ Computes the enhanced degree centrality of `vertex`, `EDC(vertex)`.

        Parameters
        ----------
        vertex : str
            Vertex for which the enhanced degree centrality is computed.

        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        Returns
        -------
        float
            `EDC(vertex)`
        """
        degree_centrality = self.degree_centrality(degree_method,vertex)
        lcc = self.local_clustering_coefficient(vertex)
        self.degree_centralities[vertex] = float(degree_centrality)
        return abs(degree_centrality*lcc)

    def successors(self, vertex: str) -> List[str]:
        """ Derives the successors of `vertex`. Those are the nodes that are connected to `vertex`, via outgoing edges from `vertex`.

        Parameters
        ----------
        vertex : str
            Vertex for which the successors are derived.

        Returns
        -------
        List[str]
            List of successors of `vertex`.
        """
        successors = self.adjacency_list[vertex]
        return successors

    def predecessors(self, vertices: List[str], vertex: str) -> List[str]:
        """ Derives the predecessors of `vertex`. Those are the nodes that are connected to `vertex`, via incoming edges to `vertex`.

        Parameters
        ----------
        vertex : str
            Vertex for which the predecessors are derived.

        vertices : List[str]
            Vertices of the original graph.


        Returns
        -------
        List[str]
            List of predecessors of `vertex`.
        """
        predecessors = [v for v in vertices if vertex in self.adjacency_list[v]]
        return predecessors

    def average_enhanced_degree_centrality(self, edcs: List[Tuple[str,float]]) -> float:
        """ Calculates the average enhanced degree centrality over `edcs`.

        Parameters
        ----------
        edcs : List[Tuple[str,float]]
            EDCs values of all nodes.

        Returns
        -------
        float
            Average EDC. 
        """
        return sum([x[1] for x in edcs])/float(len(edcs))

    def sort_by_special_degree_centrality_measures(self, metric: Callable[[Callable[[str], int],str],float],
                                                   submetric: Callable[[str], int], vertices: List[str]) -> List[Tuple[str,float]]:
        """ Computes the enhanced degree centrality of `vertex`, `EDC(vertex)`.

        Parameters
        ----------
        metric : Callable[[Callable[[str], int],str],float]
            Metric used: EDC or DC for instance.

        submetric : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        vertices : List[str]
            Vertices of the graph

        Returns
        -------
        List[Tuple[str,float]]
              A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        degrees_tuples = [(vertex, metric(submetric, vertex)) for vertex in vertices]
        degrees_sorted = sorted(degrees_tuples, key=itemgetter(1), reverse=True)
        return degrees_sorted

    def sort_nodes_by_edc(self, degree_method: Callable[[str], int], vertices: List[str]) -> List[Tuple[str,float]]:
        """ Sorts the nodes by EDC value.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        vertices : List[str]
            Vertices of the graph

        Returns
        -------
        List[Tuple[str,float]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its EDC value.
        """
        return self.sort_by_special_degree_centrality_measures(self.enhanced_degree_centrality,degree_method,vertices)

    def sort_nodes_by_degree_centrality(self,degree_method: Callable[[str], int], vertices: List[str]) -> List[Tuple[str,float]]:
        """Sorts the nodes by DC value.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        vertices : List[str]
            Vertices of the graph

        Returns
        -------
        List[Tuple[str,float]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its DC value.
        """
        return self.sort_by_special_degree_centrality_measures(self.degree_centrality,degree_method,vertices)

    def filter_out_nodes_edc_threshold(self, nodes_tuples: List[Tuple[str,float]], threshold: float) -> List[str]:
        """ Filters out the given nodes by their degree centrality value being greater than `threshold` or not.

        Parameters
        ----------
        nodes_tuples : List[Tuple[str,float]]
            A list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its EDC value.

        threshold : float
            Threshold for filtering out nodes.
            If the degree centrality of a node `v` is below that threshold, then `v` is filtered out.

        Returns
        -------
        List[str]
            List of filtered nodes.
        """
        final_nodes = [x[0] for x in nodes_tuples if self.degree_centralities[x[0]] >= threshold]
        print(final_nodes)
        return final_nodes

    def active_nodes(self, nodes_list: List[str]) -> List[str]:
        """ Returns the top quarter of `nodes_list`, which correspond to the nodes with the 25% biggest EDC values.

        Parameters
        ----------
        nodes_list : List[str]
            List of nodes.

        Returns
        -------
        List[str]
            Top quarter of `nodes_list`
        """
        quarter = math.ceil(len(nodes_list)/4)
        print(quarter)
        return nodes_list[0:quarter]

    def get_influential_nodes(self, degree_method: Callable[[str], int]) -> List[str]:
        """ Computes the influential nodes in `self` using the IM algorithm.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            Degree metric used: in-degree or out-degree.

        Returns
        -------
        List[str]
            List of influential nodes.
        """
        graph_nodes = self.nodes
        if self.most_connected_node is None:
            self.most_connected_node = self.mcn(degree_method)
        edcs = self.sort_nodes_by_edc(degree_method,graph_nodes)
        average_edc = self.average_enhanced_degree_centrality(edcs)
        fn = self.filter_out_nodes_edc_threshold(edcs,average_edc)
        return self.active_nodes(fn)

    def select_random_nodes(self,k):
        """ Retrieve case ID from file name.

        Parameters
        ----------
        path : str
            Name of the test file to retrieve the case ID from.

        Returns
        -------
        al : dict
            A list of split file name with case ID in it.
        """
        vertices = self.get_vertices()
        selected_nodes = random.sample(vertices,k=k)
        return selected_nodes

    def get_subgraph(self, nodes):
        """ Retrieve case ID from file name.

        Parameters
        ----------
        path : str
            Name of the test file to retrieve the case ID from.

        Returns
        -------
        al : dict
            A list of split file name with case ID in it.
        """
        new_al = {}
        for node in nodes:
            out_nodes = [out_node for out_node in self.adjacency_list[node] if out_node in nodes]
            new_al[node] = out_nodes
        return new_al

    def return_full_subgraph(self, number_of_nodes,degree_method_string):
        """ Retrieve case ID from file name.

        Parameters
        ----------
        path : str
            Name of the test file to retrieve the case ID from.

        Returns
        -------
        Graph
            A list of split file name with case ID in it.
        """
        new_al = self.get_subgraph(self.select_random_nodes(number_of_nodes))
        sub = Graph("", new_al)
        degree_method = sub.in_degree if degree_method_string == "i" else sub.out_degree
        sub.most_connected_node = sub.mcn(degree_method)
        return sub

    def return_full_subgraph2(self, nodes):
        """ Retrieve case ID from file name.

        Parameters
        ----------
        path : str
            Name of the test file to retrieve the case ID from.

        Returns
        -------
        al : dict
            A list of split file name with case ID in it.
        """
        new_al = self.get_subgraph(nodes)
        sss = Graph("", new_al)
        return sss


def generate_random_graph():
    """ Retrieve case ID from file name.

    Parameters
    ----------
    path : str
        Name of the test file to retrieve the case ID from.

    Returns
    -------
    al : dict
        A list of split file name with case ID in it.
    """
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
    """ Retrieve case ID from file name.

    Parameters
    ----------
    path : str
        Name of the test file to retrieve the case ID from.

    Returns
    -------
    al : dict
        A list of split file name with case ID in it.
    """
    file = list(filename)
    dot_index = file.index(".")
    file_type = "".join(filename[dot_index+1:])
    return file_type


def store_influential_nodes(path, nodes):
    """ Retrieve case ID from file name.

    Parameters
    ----------
    path : str
        Name of the test file to retrieve the case ID from.

    Returns
    -------
    al : dict
        A list of split file name with case ID in it.
    """
    with open(path, 'w') as output_file:
        for index, node in enumerate(nodes):
            output_file.write(node)
            if index != len(nodes) - 1:
                output_file.write("\n")


def write_graph_txt_file(path,g):
    """ Retrieve case ID from file name.

    Parameters
    ----------
    path : str
        Name of the test file to retrieve the case ID from.

    Returns
    -------
    al : dict
        A list of split file name with case ID in it.
    """
    with open(path, 'w') as output_file:
        edges = g.edges
        for index, edge in enumerate(edges):
            output_file.write(edge[0] + " " + edge[1])
            if index != len(edges) - 1:
                output_file.write("\n")


if __name__ == "__main__":
    g = Graph("../wiki-Vote.txt")
    s = g.return_full_subgraph(1000,"o")
    seeds = s.get_influential_nodes(s.out_degree)
    lt = lt.LinearThresholdModel(s, seeds)





