'''
 * Copyright (c) 2020, Rutgers University
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * + Redistributions of source code must retain the above copyright notice,
 *   this list of conditions and the following disclaimer.
 * + Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
'''

import collections
import random

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
        :param path: the file path to access the topology
        :return: the graph of the underlying network
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
        '''
        Create the nodes and the links based on the underlying network graph
        :return: the created network topology
        '''
        # create nodes
        for n in self.graph:
            self.nodes[n] = Node(n)

        # create links
        for n in self.graph:
            for nei in self.graph[n]:
                a, b = self.nodes[n], self.nodes[nei]
                self.topology[a].append(b)

                # todo: to find a model to specify link bandwidth and latency
                propagation_latency = abs(random.gauss(2, 1))
                self.links[a.id, b.id] = Link(a, b, 100, propagation_latency)

        return self.topology

    def get_links(self):
        return self.links

    def get_nodes(self):
        '''
        To get the vertex in the graph.
        :return:
        '''
        return list(self.topology.keys())


if __name__ == '__main__':
    t = Topology()
    graph = t.load_network_graph(path= './topology/topology.txt')
    t.create_network_topology()
    print(t.topology)

