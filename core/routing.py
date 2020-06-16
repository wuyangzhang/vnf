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

The routing module that find the shortest path between VNF servers
'''


def cal_shortest_path(graph, link):
    '''
    Apply Dijkstra to each node in the graph..
    :param graph:
    :param link:
    :return:
    '''
    nodes = graph.keys()
    paths = {}
    for n in nodes:
        dist, prev = dijkstra(graph, link, n)
        paths[n.id] = prev
    return paths


def dijkstra(graph, link, source):
    '''
    Use the link latency as the routing metric to find the shortest path
    :param graph:
    :param link:
    :param source:
    :return:
    '''
    dist = {}
    prev = {}
    nodes = set()
    for n in graph.keys():
        dist[n] = float('inf')
        prev[n.id] = -1
        nodes.add(n)
    dist[source] = 0

    while nodes:
        min_dist = float('inf')
        target = -1
        for n in nodes:
            if min_dist > dist[n]:
                min_dist = dist[n]
                target = n

        nodes.remove(target)

        for nei in graph[target]:
            alt = dist[target] + link[target.id, nei.id].latency
            if dist[nei] > alt:
                dist[nei] = alt
                prev[nei.id] = target.id

    return dist, prev


def find_shortest_path(paths, source, destination):
    '''
    Output the path between the source and the destination.
    :param paths:
    :param source:
    :param destination:
    :return:
    '''
    path = [destination]
    cur = destination
    while cur != source:
        cur = paths[source][cur]
        path.insert(0, cur)
    return path
