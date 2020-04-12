import copy
import random


class IndependentCascadeModel:

    def __init__(self, g, seeds, act_prob):
        self.cascade(g, seeds, act_prob)

    @staticmethod
    def prop_success(act_prob):
        random_number = round(random.random(), 1)
        return random_number <= act_prob

    def diffuse_one_round(self, g, seed_nodes, tried_edges, act_prob):
        activated_nodes_of_this_round = set()
        tried_edges_of_this_round = set()
        for s in seed_nodes:
            nbs = g.successors(s)
            for nb in nbs:
                if nb in seed_nodes or (s, nb) in tried_edges or (s, nb) in tried_edges_of_this_round:
                    continue
                if self.prop_success(act_prob):
                    activated_nodes_of_this_round.add(nb)
                tried_edges_of_this_round.add((s, nb))
        activated_nodes_of_this_round = list(activated_nodes_of_this_round)
        seed_nodes.extend(activated_nodes_of_this_round)
        return seed_nodes, activated_nodes_of_this_round, tried_edges_of_this_round

    def diffuse_all(self, g, seed_nodes, act_prob):
        tried_edges = set()
        layer_i_nodes = [[i for i in seed_nodes]]
        total_influenced_nodes = len(layer_i_nodes[0])
        while True:
            len_old = len(seed_nodes)
            (seed_nodes, activated_nodes_of_this_round, tried_edges_of_this_round) = \
                self.diffuse_one_round(g, seed_nodes, tried_edges, act_prob)
            layer_i_nodes.append(activated_nodes_of_this_round)
            total_influenced_nodes += len(activated_nodes_of_this_round)
            tried_edges = tried_edges.union(tried_edges_of_this_round)
            if len(seed_nodes) == len_old:
                break
        return layer_i_nodes,total_influenced_nodes

    def cascade(self, g, seeds, act_prob):
        for s in seeds:
            if s not in g.get_vertices():
                raise Exception("seed", s, "is not in graph")

        # init activation probabilities
        if act_prob > 1:
          raise Exception("edge activation probability cannot be larger than 1")

        # perform diffusion
        seed_nodes = copy.deepcopy(seeds)  # prevent side effect
        return self.diffuse_all(g, seed_nodes, act_prob)
