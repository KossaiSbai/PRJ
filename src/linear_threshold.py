
import copy


def _diffuse_one_round(g ,seed_nodes, influences, thresholds):
    activated_nodes_of_this_round = set()
    all_vertices = g.nodes
    for s in seed_nodes:
        nbs = g.successors(s)
        for nb in nbs:
            if nb in seed_nodes:
                continue
            active_nb = list(set(g.predecessors(all_vertices,nb)).intersection(set(seed_nodes)))
            if _influence_sum(active_nb, influences) >= thresholds[nb]:
                activated_nodes_of_this_round.add(nb)
    activated_nodes_of_this_round = list(activated_nodes_of_this_round)
    seed_nodes.extend(activated_nodes_of_this_round)
    return seed_nodes, activated_nodes_of_this_round


def _diffuse_all(G,A,influences,thresholds):
    layer_i_nodes = []
    layer_i_nodes.append([i for i in A])
    total_influenced_nodes = len(layer_i_nodes[0])
    while True:
        len_old = len(A)
        (A, activated_nodes_of_this_round) = _diffuse_one_round(G, A,influences, thresholds)
        total_influenced_nodes+=len(activated_nodes_of_this_round)
        layer_i_nodes.append(activated_nodes_of_this_round)
        if len(A) == len_old:
            break
    return layer_i_nodes,total_influenced_nodes


# def _diffuse_k_rounds( G, seed_nodes, influences, thresholds, steps):
#     layer_i_nodes = []
#     layer_i_nodes.append([i for i in seed_nodes])
#     vertices = G.get_vertices()
#     while steps > 0 and len(seed_nodes) < len(vertices):
#         len_old = len(seed_nodes)
#         (seed_nodes, activated_nodes_of_this_round) = \
#             _diffuse_one_round(G, seed_nodes, influences, thresholds)
#         layer_i_nodes.append(activated_nodes_of_this_round)
#         if len(seed_nodes) == len_old:
#             break
#         steps -= 1
#     return layer_i_nodes


def cascade(g, seeds, steps):
    influences = {}
    thresholds = {}
    for s in seeds:
        if s not in g.get_vertices():
            raise Exception('seed', s, 'is not in graph')

    for n in g.get_vertices():
        ind = g.in_degree(n)
        influences[n] = 1 if ind == 0 else 1 / float(ind)
        thresholds[n] = 0.5

    # perform diffusion

    seed_nodes = copy.deepcopy(seeds)  # prevent side effect
    if steps <= 0:
        return _diffuse_all(g, seed_nodes, influences, thresholds)

    return _diffuse_k_rounds(g, seed_nodes, influences, thresholds,
                             steps)


def _influence_sum(froms, influences):
    influence_sum = 0.0
    for f in froms:
        influence_sum += influences[f]
    return influence_sum
