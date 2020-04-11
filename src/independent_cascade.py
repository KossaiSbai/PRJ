import copy
import random


def _prop_success(act_prob):
    random_number = round(random.random(), 1)
    return random_number <= act_prob


def _diffuse_one_round(g, seed_nodes, tried_edges, act_prob):
    activated_nodes_of_this_round = set()
    tried_edges_of_this_round = set()
    for s in seed_nodes:
        nbs = g.successors(s)
        for nb in nbs:
            if nb in seed_nodes or (s, nb) in tried_edges or (s, nb) in tried_edges_of_this_round:
                continue
            if _prop_success(act_prob):
                activated_nodes_of_this_round.add(nb)
            tried_edges_of_this_round.add((s, nb))
    activated_nodes_of_this_round = list(activated_nodes_of_this_round)
    seed_nodes.extend(activated_nodes_of_this_round)
    return seed_nodes, activated_nodes_of_this_round, tried_edges_of_this_round


def _diffuse_all(g, seed_nodes, act_prob):
    tried_edges = set()
    layer_i_nodes = [[i for i in seed_nodes]]
    total_influenced_nodes = len(layer_i_nodes[0])
    while True:
        len_old = len(seed_nodes)
        (seed_nodes, activated_nodes_of_this_round, tried_edges_of_this_round) = \
            _diffuse_one_round(g, seed_nodes, tried_edges, act_prob)
        layer_i_nodes.append(activated_nodes_of_this_round)
        total_influenced_nodes += len(activated_nodes_of_this_round)
        tried_edges = tried_edges.union(tried_edges_of_this_round)
        print("SSSS",seed_nodes)
        if len(seed_nodes) == len_old:
          break
    return layer_i_nodes,total_influenced_nodes


def _diffuse_k_rounds(g, seed_nodes, steps, act_prob):
    tried_edges = set()
    layer_i_nodes = []
    layer_i_nodes.append([i for i in seed_nodes])
    number_of_vertices = len(g.get_vertices())
    while steps > 0 and len(seed_nodes) < number_of_vertices:
        len_old = len(seed_nodes)
        A, activated_nodes_of_this_round, cur_tried_edges = _diffuse_one_round(g, seed_nodes, tried_edges, act_prob)
        layer_i_nodes.append(activated_nodes_of_this_round)
        tried_edges = tried_edges.union(cur_tried_edges)
        if len(A) == len_old:
            break
        steps -= 1
    return layer_i_nodes


def cascade(g, seeds, act_prob, steps):
    for s in seeds:
        if s not in g.get_vertices():
            raise Exception("seed", s, "is not in graph")

    # init activation probabilities
    if act_prob > 1:
      raise Exception("edge activation probability cannot be larger than 1")

    # perform diffusion
    seed_nodes = copy.deepcopy(seeds)  # prevent side effect
    if steps <= 0:
    # perform diffusion until no more nodes can be activated
        return _diffuse_all(g, seed_nodes, act_prob)
    # perform diffusion for at most "steps" rounds
    return _diffuse_k_rounds(g, seed_nodes, steps, act_prob)


