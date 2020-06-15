import collections

import numpy as np

from .node import Node
from .link import Link


class Topology:
    def __init__(self):
        self.graph = collections.defaultdict(set)
        self.topology = collections.defaultdict(list)
        self.nodes = dict() # key: node_id, value: node
        self.links = dict() # key: (from, to), value: link

    def load_network_graph(self, path):
        '''
        load the AT&T network topology from http://www.topology-zoo.org/files/AttMpls.gml
        :param path:
        :return: network topology
        '''
        with open(path) as f:
            src = -1
            for line in f.readlines():
                line = line.strip()
                if 'source' in line:
                    src = int(line.split(' ')[1])
                elif 'target' in line:
                    dest = int(line.split(' ')[1])
                    self.graph[src].add(dest)
                    self.graph[dest].add(src)
        return self.graph

    def create_network_topology(self):
        for n in self.graph:
            self.nodes[n] = Node(n)

        # add nodes and links
        for n in self.graph:
            for nei in self.graph[n]:
                a, b = self.nodes[n], self.nodes[nei]
                self.topology[a].append(b)

                # need to specify link bandwidth and latency
                latency = np.random.poisson(40, 1)[0]
                self.links[a, b] = Link(a, b, 100, latency)

        return self.topology

    def get_nodes(self):
        return list(self.topology.keys())


if __name__ == '__main__':
    t = Topology()
    graph = t.load_network_graph(path= './topology/topology.txt')
    t.create_network_topology()
    print(t.topology)

