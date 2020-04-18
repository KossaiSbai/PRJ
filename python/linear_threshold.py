import copy
from typing import List,Tuple,Dict
from python.graph import Graph

# The below reference is a python implementation of the LT model. It is reused for the implementation of this class.
# Hung-Hsuan Chen (19 nov 2016) linear_threshold.py source code [Source code]. https://github.com/hhchen1105/networkx_addon/blob/master/information_propagation/linear_threshold.py

class LinearThresholdModel:
    """Linear Threshold model class

    Parameters
    ----------
    g : Graph
        graph on which LT is performed.

    seeds : List[str]
         list of seed nodes
    """

    def __init__(self, g, seeds):
        self.all_influenced_nodes = [[]]
        self.total_number_of_nodes = 0
        self.all_influenced_nodes, self.total_number_of_nodes = self.cascade(g,seeds)

    def get_influenced_nodes(self):
        """Returns a list of all the influenced nodes at the end of the diffusion process.

        Returns
        -------
        List[List[str]]
            list of influenced nodes.
        """
        return self.all_influenced_nodes

    def get_total_number_of_influenced_nodes(self):
        """Returns the total number of influenced nodes after carrying out the diffusion process.

        Returns
        -------
        int
            number of influenced nodes.
        """
        return self.total_number_of_nodes

    @staticmethod
    def compute_influence_sum(froms: List[str], influences: Dict[str, float]) -> float:
        """ Computes the total sum of the influences of the seed nodes.

        Parameters
        ----------
        froms :  List[str]
            list of seed nodes.

        influences :  Dict[str,float]
            dictionary which entries (`v`, `i`) associate each node `v` to its influence value `e`.

        Returns
        -------
        float
            the total sum of the influences of the seed nodes.
        """
        influence_sum = sum([influences[f] for f in froms])
        return influence_sum

    def diffuse_one_round(self, g: Graph , seed_nodes: List[str], influences: Dict[str, float], thresholds: Dict[str, float]) -> Tuple[List[str],List[str]]:
        """ Executes the diffusion process for one round.

        Parameters
        ----------
        g :  Graph
             graph on which LT is performed.

        seed_nodes : List[str]
            list of seed nodes.

        influences : Dict[str, float]
            dictionary which entries (`v`, `i`) associate each node `v` to its influence value `e`.

        thresholds : Dict[str, float]
             dictionary which entries (`v`, `t`) associate each node `v` to its threshold value `t`.

        Returns
        -------
        Tuple[List[str],List[str]]
            The list of the new seed nodes as well as a list of the nodes that got influenced at the given round.
        """
        activated_nodes_of_this_round = set()
        all_vertices = g.nodes
        for s in seed_nodes:
            nbs = g.successors(s)
            for nb in nbs:
                if nb in seed_nodes:
                    continue
                # Extracts the predecessors of nb that are seed nodes.
                active_nb = list(set(g.predecessors(all_vertices,nb)).intersection(set(seed_nodes)))
                if self.compute_influence_sum(active_nb, influences) >= thresholds[nb]:
                    activated_nodes_of_this_round.add(nb)
        activated_nodes_of_this_round = list(activated_nodes_of_this_round)
        seed_nodes.extend(activated_nodes_of_this_round)
        return seed_nodes, activated_nodes_of_this_round

    def diffuse_all(self, g: Graph, seed_nodes: List[str], influences:  Dict[str, float], thresholds:  Dict[str, float]) -> Tuple[List[List[str]], int]:
        """ Executes the diffusion process until no more nodes can be influenced.

        Parameters
        ----------
        g :  Graph
            graph on which LT is performed.

        seed_nodes : List[str]
            list of seed nodes.

        influences : Dict[str, float]
            a dictionary which entries (`v`, `i`) associate each node `v` to its influence value `e`.

        thresholds : Dict[str, float]
            a dictionary which entries (`v`, `t`) associate each node `v` to its threshold value `t`.

        Returns
        -------
        Tuple[List[List[str]], int]
            list of lists of influenced nodes as well as the total number of influenced nodes.
        """
        # Each sublist at index i stores the nodes influenced at round i.
        # So initially, at round 0, the seed nodes are the only influenced nodes.
        layer_i_nodes = [[i for i in seed_nodes]]
        total_influenced_nodes = len(layer_i_nodes[0])
        while True:
            len_old = len(seed_nodes)
            (seed_nodes, activated_nodes_of_this_round) = self.diffuse_one_round(g, seed_nodes, influences, thresholds)
            total_influenced_nodes += len(activated_nodes_of_this_round)
            layer_i_nodes.append(activated_nodes_of_this_round)
            # If no more nodes have been influenced at the round that has just happened, the process halts.
            if len(seed_nodes) == len_old:
                break
        return layer_i_nodes,total_influenced_nodes

    def cascade(self, g: Graph, seeds: List[str]) -> Tuple[List[List[str]], int]:
        """ Executes the LT diffusion process.

        Parameters
        ----------
        g :  Graph
            graph on which LT is performed.

        seeds : List[str]
            list of seed nodes.
        Returns
        -------
        Tuple[List[List[str]], int]
            list of lists of influenced nodes as well as the total number of influenced nodes.
        """
        influences = {}
        thresholds = {}
        for s in seeds:
            if s not in g.get_vertices():
                raise Exception('seed', s, 'is not in graph')

        # Initialises the influences and thresholds
        for n in g.get_vertices():
            ind = g.in_degree(n)
            influences[n] = 1 if ind == 0 else 1 / float(ind)
            thresholds[n] = 0.5

        seed_nodes = copy.deepcopy(seeds)  # prevent side effect
        return self.diffuse_all(g, seed_nodes, influences, thresholds)




