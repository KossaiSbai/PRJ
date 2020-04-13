from operator import itemgetter
import math
import random
from typing import List,Callable,Tuple,Dict
import itertools


class Graph:

    """Conceptual class representing a graph data structure

    Parameters
    ----------
    path : str, optional
        path of the txt file. Defaults to "".

    al : dict, optional
        adjacency list. Defaults to None.
    """

    def __init__(self, path="", al=None):
        """
        Constructor method.
        """
        self.adjacency_list = {}
        self.nodes = []
        if path != "":
            self.process_tgf_file(path) if return_file_type(path) == "tgf" else self.process_txt_file(path)
        else:
            self.adjacency_list = al
            self.nodes = self.get_vertices()
        self.edges = self.get_edges()
        self.most_connected_node_degree_value = None
        self.degree_centralities = {}

    def get_edges(self) -> List[Tuple[str, str]]:
        """Extracts and returns the edges of `self`.

        Returns
        -------
        List[Tuple[str,str]]
            list of tuples where each tuple (`a`, `b`) is an edge between `a` and `b`.
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
            list of strings where each string `v`, is a node `v` of the graph.
        """

        return list(self.adjacency_list.keys())

    def get_adjacency_list(self) -> Dict[str,List[str]]:
        """Extracts and returns the adjacency list of `self`.

        Returns
        -------
        Dict[str,List[str]]
            dictionary which entries (`v`, `e`) associate each node `v` to its outgoing nodes `e`.
        """

        return self.adjacency_list

    def build_adjacency_list(self, lines: List[str]) -> Dict[str,List[str]]:
        """ Builds the adjacency list of `self` from the content of a file (txt or tgf).

        Parameters
        ----------
        lines :  List[str]
            list of strings (`a`, `b`) denoting an edge between `a` and `b`.

        Returns
        -------
        Dict[str,List[str]]
            the adjacency list of `self`.
        """
        for x in lines:
            # Splits the line by whitespace and gets the two nodes of the edge.
            end_nodes = x.split(" ")
            from_node = end_nodes[0]
            to_node = end_nodes[1]
            # Skips if the two nodes are the same: avoid self loops.
            if from_node == to_node:
                continue
            if from_node not in self.adjacency_list.keys():
                self.adjacency_list[from_node] = [to_node]
            else:
                self.adjacency_list[from_node].append(to_node)
            # If the tail node of the edge is not the adjacency list then make its adjacency list empty.
            if to_node not in self.adjacency_list.keys():
                self.adjacency_list[to_node] = []

        return self.adjacency_list

    def process_tgf_file(self, path: str) -> None:
        """ Builds and stores the graph from a tgf file.

        Parameters
        ----------
        path : str
            path of the tgf file.
        """
        # split() gets rid of tab characters.
        line_list = [' '.join(line.split()) for line in open(path, "r")]
        hashtag_index = line_list.index("#")
        # Extracts the nodes part and the edges part separated by the # symbol.
        nodes_part = line_list[:hashtag_index]
        edges_part = line_list[hashtag_index+1:]
        self.adjacency_list = self.build_adjacency_list(edges_part)
        self.nodes = [nodes_part[i].split(" ")[0] for i in range(len(nodes_part))]

    def process_txt_file(self, path: str) -> None:
        """  Builds and stores the graph from a txt file.

        Parameters
        ----------
        path : str
            path of the txt file.
        """
        line_list = [' '.join(line.split()) for line in open(path, "r")]
        self.adjacency_list = self.build_adjacency_list(line_list)
        self.nodes = self.get_vertices()

    def in_degree(self, vertex: str) -> int:
        """ Calculates the in-degree of the `vertex`.

        Parameters
        ----------
        vertex : str
            vertex for which the in-degree is calculated.

        Returns
        -------
        int
            the in-degree of the vertex.
        """
        in_neighbours = [node for node in self.nodes if vertex in self.adjacency_list[node]]
        return len(in_neighbours)

    def out_degree(self, vertex: str) -> int:
        """ Calculates the out-degree of the `vertex`.

        Parameters
        ----------
        vertex : str
            vertex for which the out-degree is calculated.

        Returns
        -------
        int
            the out-degree of the vertex.
        """
        return len(self.adjacency_list[vertex])

    @staticmethod
    def compute_degrees(degree_method: Callable[[str], int], vertices: List[str]) -> List[Tuple[str, int]]:
        """ Computes and stores the degree values for each node, using the given degree metric.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        vertices : List[str]
            list of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        degrees_tuples = [(vertex, degree_method(vertex)) for vertex in vertices]
        return degrees_tuples

    def sort_vertices_by_degree(self, degree_method: Callable[[str], int], vertices: List[str]) -> List[Tuple[str, int]]:
        """Sorts the nodes by degree value.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        vertices : List[str]
            list of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        degrees_tuples = self.compute_degrees(degree_method, vertices)
        # Sorts the list of tuples by degree (second element of the tuple) in reverse order, that is decreasing order.
        degrees_sorted = sorted(degrees_tuples, key=itemgetter(1), reverse=True)
        return degrees_sorted

    def compute_in_degrees(self, vertices: List[str]) -> List[Tuple[str, int]]:
        """ Computes and stores the in-degree values for each node.

        Parameters
        ----------
        vertices : List[str]
            list of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        return self.compute_degrees(self.in_degree, vertices)

    def sort_vertices_by_in_degree(self, vertices: List[str]) -> List[Tuple[str, int]]:

        """ Sorts the nodes by in-degree value.

        Parameters
        ----------
        vertices : List[str]
            list of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its in-degree value.
        """
        return self.sort_vertices_by_degree(self.in_degree, vertices)

    def compute_out_degrees(self, vertices: List[str]) -> List[Tuple[str, int]]:
        """ Computes and stores the out-degree values for each node.

        Parameters
        ----------
        vertices : List[str]
            list of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        return self.compute_degrees(self.out_degree, vertices)

    def sort_vertices_by_out_degree(self, vertices: List[str]) -> List[Tuple[str, int]]:
        """ Sorts the nodes by out-degree value.

        Parameters
        ----------
        vertices : List[str]
            list of nodes.

        Returns
        -------
        List[Tuple[str,int]]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its out-degree value.
        """
        return self.sort_vertices_by_degree(self.out_degree, vertices)

    def select_vertices_with_k_biggest_degree_values(self, degree_method:  Callable[[str], int], k: int) -> List[str]:
        """ Select the vertices of `self` with the `k` biggest degree values.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        k : int
           number of vertices to be selected.

        Returns
        -------
         List[str]
            list of selected vertices.
        """
        degrees_sorted = self.sort_vertices_by_degree(degree_method, self.nodes)
        return [degree_tuple[0] for degree_tuple in degrees_sorted][0:k]

    def neighbourhood(self, vertex: str) -> List[str]:
        """ Determines the neighbourhood of `vertex`, which are the nodes connected to `vertex` by either an outgoing or incoming edge.

        Parameters
        ----------
        vertex : str
            vertex which neighbourhood is determined.

        Returns
        -------
        List[str]
            list of nodes corresponding to the neighbourhood of `vertex`.
        """
        nodes = self.adjacency_list.keys()
        neighbours = [node for node in nodes if node in self.adjacency_list[vertex] or vertex in self.adjacency_list[node]]
        return neighbours

    def number_of_edges_within_neighbourhood(self, neighbourhood: List[str]) -> int:
        """ Determines the number of edges linking nodes in a given neighbourhood.

        Parameters
        ----------
        neighbourhood : List[str]
            list of neighbours.

        Returns
        -------
        int
            number of edges within neighbourhood.
        """
        neighbourhood_edges = 0
        for neighbour in neighbourhood:
            # Derives the number of nodes that are both in neighbourhood and in the adjacency list associated to the node called neighbour.
            neighbourhood_edges += len(list(set(neighbourhood) & set(self.adjacency_list[neighbour])))
        return neighbourhood_edges

    def local_clustering_coefficient(self, vertex: str) -> float:
        """ Computes the local clustering coefficient of `vertex`, `LCC(vertex)`.

        Parameters
        ----------
        vertex : str
            vertex for which the local clustering coefficient is computed.

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
            vertex for which the  node level centrality is computed.
        
        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        Returns
        -------
        float
            `NLC(vertex)`
        """
        neighbours = self.neighbourhood(vertex)
        neighbours.append(vertex)
        degrees = self.sort_vertices_by_degree(degree_method, neighbours)
        # Gets the biggest degree value in the neighbourhood.
        # This corresponds to the second element (degree value) of the first tuple of the sorted list since it is sorted in decreasing order.
        most_connections = degrees[0][1]
        degree_centrality = sum([most_connections - degree[1] for degree in degrees])
        return degree_centrality

    def compute_biggest_degree_value(self, degree_method: Callable[[str], int]) -> int:
        """ Iterates through the nodes in `self` and retrieves the biggest degree value.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        Returns
        -------
        int
            biggest degree value in the given graph.
        """
        biggest_degree_value = self.sort_vertices_by_degree(degree_method, self.get_vertices())[0][1]
        return biggest_degree_value

    def degree_centrality(self, degree_method: Callable[[str], int], vertex: str) -> float:
        """ Computes the degree centrality of `vertex`, `DC(vertex)`.

        Parameters
        ----------
        vertex : str
            vertex for which the  degree centrality is computed.

        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        Returns
        -------
        float
            `DC(vertex)`
        """
        node_level_centrality = self.node_level_centrality(degree_method, vertex)
        if node_level_centrality != 0:
            return (self.most_connected_node_degree_value - degree_method(vertex)) / node_level_centrality
        else:
            return self.most_connected_node_degree_value - degree_method(vertex)

    def enhanced_degree_centrality(self, degree_method: Callable[[str], int], vertex: str) -> float:
        """ Computes the enhanced degree centrality of `vertex`, `EDC(vertex)`.

        Parameters
        ----------
        vertex : str
            vertex for which the enhanced degree centrality is computed.

        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        Returns
        -------
        float
            `EDC(vertex)`
        """
        degree_centrality = self.degree_centrality(degree_method, vertex)
        lcc = self.local_clustering_coefficient(vertex)
        self.degree_centralities[vertex] = float(degree_centrality)
        return abs(degree_centrality*lcc)

    def successors(self, vertex: str) -> List[str]:
        """ Derives the successors of `vertex`. Those are the nodes that are connected to `vertex`, via outgoing edges from `vertex`.

        Parameters
        ----------
        vertex : str
            vertex for which the successors are derived.

        Returns
        -------
        List[str]
            list of successors of `vertex`.
        """
        successors = self.adjacency_list[vertex]
        return successors

    def predecessors(self, vertices: List[str], vertex: str) -> List[str]:
        """ Derives the predecessors of `vertex`. Those are the nodes that are connected to `vertex`, via incoming edges to `vertex`.

        Parameters
        ----------
        vertex : str
            vertex for which the predecessors are derived.

        vertices : List[str]
            vertices of the original graph.


        Returns
        -------
        List[str]
            list of predecessors of `vertex`.
        """
        predecessors = [v for v in vertices if vertex in self.adjacency_list[v]]
        return predecessors

    @staticmethod
    def average_enhanced_degree_centrality(edcs: List[Tuple[str, float]]) -> float:
        """ Calculates the average enhanced degree centrality over `edcs`.

        Parameters
        ----------
        edcs : List[Tuple[str,float]]
            EDCs values of all nodes.

        Returns
        -------
        float
            average EDC.
        """
        return sum([x[1] for x in edcs])/float(len(edcs))

    @staticmethod
    def sort_by_advanced_degree_centrality_metric(advanced_metric: Callable[[Callable[[str], int], str], float],
                                                  basic_metric: Callable[[str], int], vertices: List[str]) -> List[Tuple[str, float]]:
        """ Sorts the nodes by degree values computed via an advanced degree metric such as `EDC` or `DC`.

        Parameters
        ----------
        advanced_metric : Callable[[Callable[[str], int],str],float]
            advanced degree metric used: EDC or DC for instance.

        basic_metric : Callable[[str], int]
            basic degree metric used: in-degree or out-degree.

        vertices : List[str]
            vertices of the graph.

        Returns
        -------
        List[Tuple[str,float]]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its degree value.
        """
        # The advanced metric takes the basic metric as parameter.
        # For instance, EDC takes out-degree or in-degree as parameter.
        degrees_tuples = [(vertex, advanced_metric(basic_metric, vertex)) for vertex in vertices]
        degrees_sorted = sorted(degrees_tuples, key=itemgetter(1), reverse=True)
        return degrees_sorted

    def sort_nodes_by_edc(self, degree_method: Callable[[str], int], vertices: List[str]) -> List[Tuple[str, float]]:
        """ Sorts the nodes by EDC value.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        vertices : List[str]
            vertices of the graph.

        Returns
        -------
        List[Tuple[str,float]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its EDC value.
        """
        return self.sort_by_advanced_degree_centrality_metric(self.enhanced_degree_centrality, degree_method, vertices)

    def sort_nodes_by_degree_centrality(self,degree_method: Callable[[str], int], vertices: List[str]) -> List[Tuple[str, float]]:
        """Sorts the nodes by DC value.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        vertices : List[str]
            vertices of the graph.

        Returns
        -------
        List[Tuple[str,float]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its DC value.
        """
        return self.sort_by_advanced_degree_centrality_metric(self.degree_centrality, degree_method, vertices)

    def filter_out_nodes_edc_threshold(self, nodes_tuples: List[Tuple[str,float]], threshold: float) -> List[str]:
        """ Filters out the given nodes by their degree centrality value being greater than `threshold` or not.

        Parameters
        ----------
        nodes_tuples : List[Tuple[str,float]]
            list of tuples (`v`, `d`) where `v` is a given vertex and `d` is its EDC value.

        threshold : float
            threshold for filtering out nodes.
            If the degree centrality of a node `v` is below that threshold, then `v` is filtered out.

        Returns
        -------
        List[str]
            list of filtered nodes.
        """
        final_nodes = [x[0] for x in nodes_tuples if self.degree_centralities[x[0]] >= threshold]
        return final_nodes

    @staticmethod
    def active_nodes(nodes_list: List[str]) -> List[str]:
        """ Returns the top quarter of `nodes_list`, which correspond to the nodes with the 25% biggest EDC values.

        Parameters
        ----------
        nodes_list : List[str]
            list of nodes.

        Returns
        -------
        List[str]
            top quarter of `nodes_list`.
        """
        quarter = math.ceil(len(nodes_list)/4)
        return nodes_list[0:quarter]

    def get_influential_nodes(self, degree_method: Callable[[str], int]) -> List[str]:
        """ Computes the influential nodes in `self` using the IM algorithm.

        Parameters
        ----------
        degree_method : Callable[[str], int]
            degree metric used: in-degree or out-degree.

        Returns
        -------
        List[str]
            list of influential nodes.
        """
        graph_nodes = self.nodes
        if self.most_connected_node_degree_value is None:
            self.most_connected_node_degree_value = self.compute_biggest_degree_value(degree_method)
        edcs = self.sort_nodes_by_edc(degree_method, graph_nodes)
        average_edc = self.average_enhanced_degree_centrality(edcs)
        fn = self.filter_out_nodes_edc_threshold(edcs, average_edc)
        return self.active_nodes(fn)

    def select_random_nodes(self, k: int) -> List[str]:
        """ Returns a list of randomly selected nodes among the nodes of `self`.

        Parameters
        ----------
        k : int
            number of nodes to be selected.

        Returns
        -------
        List[str]
            list of randomly selected nodes.
        """
        vertices = self.get_vertices()
        selected_nodes = random.sample(vertices, k=k)
        return selected_nodes

    def get_adjacency_list_of_subgraph(self, nodes: List[str]) -> Dict[str, List[str]]:
        """ Builds from a set of nodes, a new adjacency list that will be associated to the subgraph which vertices are `nodes`.

        Parameters
        ----------
        nodes : str
            nodes constituting the subgraph.

        Returns
        -------
        Dict[str, List[str]]
            the adjacency list
        """
        new_al = {}
        for node in nodes:
            out_nodes = [out_node for out_node in self.adjacency_list[node] if out_node in nodes]
            new_al[node] = out_nodes
        return new_al

    def build_subgraph(self, number_of_nodes: int, degree_method_string: str) -> 'Graph':
        """ Extracts a subgraph of `self`. This subgraph's nodes are `number_of_nodes` randomly selected vertices from the nodes of `self`.

        Parameters
        ----------
        number_of_nodes : int
            number of nodes in the subgraph.

        degree_method_string : str
            string encoding the degree metric used: in-degree or our-degree.

        Returns
        -------
        Graph
            subgraph of `self`
        """
        new_al = self.get_adjacency_list_of_subgraph(self.select_random_nodes(number_of_nodes))
        sub = Graph("", new_al)
        degree_method = sub.in_degree if degree_method_string == "i" else sub.out_degree
        sub.most_connected_node_degree_value = sub.compute_biggest_degree_value(degree_method)
        return sub


def return_file_type(filename: str) -> str:
    """ Returns the file type of the file identified by `filename`.

    Parameters
    ----------
    filename : str
        name of the file.

    Returns
    -------
    str
        file type
    """
    file = list(filename)
    dot_index = file.index(".")
    file_type = "".join(filename[dot_index+1:])
    return file_type


def write_nodes_to_txt_file(path: str, nodes: List[str]) -> None:
    """Stores the vertices list `nodes` to a txt file.

    Parameters
    ----------
    path : str
        name of the txt file to write to.

    nodes : List[str]
        list of nodes to be put in the txt file.
    """
    # Reads the given file in write mode.
    with open(path, 'w') as output_file:
        for index, node in enumerate(nodes):
            output_file.write(node)
            if index != len(nodes) - 1:
                output_file.write("\n")


if __name__ == "__main__":
    import python.linear_threshold as lt
    import python.independent_cascade as ic
    g = Graph("../test_graph.txt")
    seeds = g.get_influential_nodes(g.out_degree)
    print(seeds)
    write_nodes_to_txt_file("../influential_nodes.txt",seeds)
    all_influenced_nodes = ic.IndependentCascadeModel(g, seeds,0.2).get_influenced_nodes()
    all_influenced_nodes2 = lt.LinearThresholdModel(g, seeds).get_influenced_nodes()
    influenced_nodes = all_influenced_nodes[1:len(all_influenced_nodes)]
    influenced_nodes = list(itertools.chain(*influenced_nodes))
    write_nodes_to_txt_file("../influenced_nodes.txt", influenced_nodes)
    print(all_influenced_nodes)
    print(all_influenced_nodes2)






