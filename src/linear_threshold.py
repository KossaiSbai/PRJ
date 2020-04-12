
import copy


class LinearThresholdModel:

    def __init__(self, g, seeds):
        self.cascade(g,seeds)

    @staticmethod
    def compute_influence_sum(froms, influences):
        influence_sum = sum([influences[f] for f in froms])
        return influence_sum

    def diffuse_one_round(self, g, seed_nodes, influences, thresholds):
        activated_nodes_of_this_round = set()
        all_vertices = g.nodes
        for s in seed_nodes:
            nbs = g.successors(s)
            for nb in nbs:
                if nb in seed_nodes:
                    continue
                active_nb = list(set(g.predecessors(all_vertices,nb)).intersection(set(seed_nodes)))
                if self.compute_influence_sum(active_nb, influences) >= thresholds[nb]:
                    activated_nodes_of_this_round.add(nb)
        activated_nodes_of_this_round = list(activated_nodes_of_this_round)
        print("AN",activated_nodes_of_this_round)
        seed_nodes.extend(activated_nodes_of_this_round)
        print("Seed nodes",seed_nodes)
        return seed_nodes, activated_nodes_of_this_round

    def diffuse_all(self, g, seed_nodes, influences, thresholds):
        layer_i_nodes = [[i for i in seed_nodes]]
        total_influenced_nodes = len(layer_i_nodes[0])
        print("Initial",seed_nodes)
        while True:
            len_old = len(seed_nodes)
            (seed_nodes, activated_nodes_of_this_round) = self.diffuse_one_round(g, seed_nodes, influences, thresholds)
            total_influenced_nodes += len(activated_nodes_of_this_round)
            layer_i_nodes.append(activated_nodes_of_this_round)
            if len(seed_nodes) == len_old:
                break
        return layer_i_nodes,total_influenced_nodes

    def cascade(self, g, seeds):
        influences = {}
        thresholds = {}
        for s in seeds:
            if s not in g.get_vertices():
                raise Exception('seed', s, 'is not in graph')

        for n in g.get_vertices():
            ind = g.in_degree(n)
            influences[n] = 1 if ind == 0 else 1 / float(ind)
            thresholds[n] = 0.5

        seed_nodes = copy.deepcopy(seeds)  # prevent side effect
        return self.diffuse_all(g, seed_nodes, influences, thresholds)


