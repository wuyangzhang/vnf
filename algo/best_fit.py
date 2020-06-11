from typing import List
from core.service_chain import ServiceChain
from core.server import Server

def best_fit(servers: List[Server], chains: List[ServiceChain]):
    '''
    Allocate to the server with the most available resources
    :param servers:
    :param chains:
    :return:
    '''
    for chain in chains:
        for v in chain.get_VNFs():
            # sorted servers and find the one with the most available resources
            sorted_servers = list({k: v for k, v in sorted(servers.items(), key=lambda item: (-item[1].avail_cpus, -item[1].avail_mem))}.keys())
            selected_server = servers[sorted_servers[0]]

            # attach the VNF to the selected server
            v.attach_server(selected_server)

            selected_server.attach_vnf(v)