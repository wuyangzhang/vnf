'''
the simulator to simulate the VNF scheduling and packet processing

how to write a simulator?

@network topology?
topology zoo
Jisc network
link capacity: random?

@server topology?
skip.


@server capacity?
# data center. random number 100 - 500 VMs
set the percentage of AWS nodes.
m4.xlarge
m4.large
m4.2xlarge


@packet flow?
randomly selected (start, end) pairs from the network topology.
each flow associates with 1-4 VNFs.
wikipedia trace
Arrival Process distribution


@packet routing?
how to route based on the VNF placement?
network latency model
queuing delay


@VNF: resource requirement. execution time
# resource demand: number of VM
# random (0.2, 1)


how to model execution time?
Based on VNF throughput.


@service chain?
Erd ̋os-Rényi model [48]to generate the graphs of VNF-FGs

'''

import simpy

from core.topology import Topology
from core.server import Server
from core.service_chain import ServiceChain

from algo import best_fit

def main():
    # step1: create network topology
    t = Topology()
    t.load_network_graph(path='./topology/topology.txt')
    t.create_network_topology()

    # step2: initialize servers
    servers = Server.init_servers(t.get_nodes())

    # step3: create service chains
    chains = [ServiceChain.random_gen() for _ in range(10)]

    # step4: place service chains
    best_fit(servers, chains)

    env = simpy.Environment()

    # step5: generate packets

    # step6: simulate routing process

    # step7: find the metrics


if __name__ == '__main__':
    main()
