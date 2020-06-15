from typing import List

from core.server import Server


def best_fit(servers: List[Server], chain):
    '''
    Allocate to the server with the most available resources
    :param servers:
    :param chains:
    :return:
    '''

    for v in chain.get_VNFs():
        # sorted servers and find the one with the most available resources
        sorted_servers = list({k: v for k, v in sorted(servers.items(), key=lambda item: (
        -item[1].avail_cpus, -item[1].avail_mem))}.keys())
        selected_server = servers[sorted_servers[0]]

        # selected_server.print_avail_resources()
        # print(v)
        # attach the VNF to the selected server
        if not selected_server.attach_vnf(v):
            print('Warning: Not enough available resources to attach VNF {} to server {}\n'.format(v.id,
                                                                                                   selected_server.addr))
            placed_server = []
            break
        else:
            chain.placement.append(selected_server.addr)
        print('Place vnf {} v to the server {}'.format(v.id, selected_server.addr))
    return chain


