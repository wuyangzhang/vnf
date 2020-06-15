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


A simulator to simulate the VNF scheduling and packet processing

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
Wikipedia trace
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

import random

from algo import best_fit

from core.env import env
from core.forwarding import forward_packet
from core.packet import Packet
from core.routing import *
from core.server import Server
from core.service_chain import ServiceChain
from core.topology import Topology


def flow_generator(packet_pool, servers, links):
    '''
    randomly generate a packet from the packet pool, and make it go through the placed service chain.
    :param packet_pool:
    :param servers:
    :param links:
    :return: None
    '''
    # todo: consider to find a Poisson distribution for the packet generation
    while True:
        yield env.timeout(1)
        packet = random.choice(packet_pool)
        forward_packet(packet, servers, links)

def main():
    '''
    The main control flow to run the simulation
    :return: None
    '''

    TOTAL_SERVICE_CHAIN_NUM = 4
    TOTAL_SIM_TIME = 1000

    # step1: create network topology
    t = Topology()
    t.load_network_graph(path='./topology/topology.txt')
    t.create_network_topology()

    paths = cal_shortest_path(t.topology, t.links)

    # step2: initialize servers
    servers = Server.init_servers(t.get_nodes())

    # step3: create service chains
    service_chains = [ServiceChain.random_gen() for _ in range(TOTAL_SERVICE_CHAIN_NUM)]

    # step4: place service chains
    for chain in service_chains:
        best_fit(servers, chain)

    # step5: generate a packet pool
    packet_pool = Packet.gen_packet_pool(list(servers.keys()), paths, service_chains)

    # step5.5 create a packet from the packet pool and  simulate routing process.
    env.process(flow_generator(packet_pool, servers, t.links))

    env.run(TOTAL_SIM_TIME)

    # processing delay + server queuing delay +
    # link queuing delay + link transmission delay + link propagation delay

    # step7: calculate the performance metrics
    # think about the desired metrics and how to calculate them?

if __name__ == '__main__':
    main()