
def dijkstra(graph, link, source):
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
            alt = dist[target] + link[target, nei].latency
            if dist[nei] > alt:
                dist[nei] = alt
                prev[nei.id] = target.id

    return dist, prev


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

def find_shortest_path(paths, source, destination):
    path = [destination]
    cur = destination
    while cur and cur != source:
        cur = paths[source][cur]
        path.insert(0, cur)
    return path


