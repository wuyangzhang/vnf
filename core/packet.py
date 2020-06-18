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

import random
import uuid

from .routing import find_shortest_path

random.seed(4)


class Packet:
    def __init__(self, size, src, dest, servers):
        self.id = uuid.uuid4()
        self.size = size  # Byte
        self.src_addr = src
        self.dest_addr = dest

        self.create_time = None

        self.service_chain = None
        self.routing_path = []
        self.vnf_server_addr = []
        # self.cur_addr = -1
        self.cur_addr_index = -1
        self.next_hop_addr = -1
        self.next_server_addr = -1
        self.last_processed_vnf_index = -1
        self.servers = servers

    def forward(self):
        self.cur_addr_index += 1

        cur_addr = self.get_cur_addr()
        cur_server = self.servers[cur_addr]
        cur_server.recv_packet(self)

    def is_dest_addr(self):
        return self.cur_addr_index == len(self.routing_path) - 1

    def get_cur_addr(self):
        # print(self.cur_addr_index, len(self.routing_path))
        if self.cur_addr_index < len(self.routing_path):
            return self.routing_path[self.cur_addr_index]

    def get_next_vnf_server_addr(self):
        if self.last_processed_vnf_index < len(self.service_chain.get_VNFs()) - 1:
            return self.vnf_server_addr[self.last_processed_vnf_index + 1]

    def get_next_hop_addr(self):
        if self.cur_addr_index < len(self.routing_path) - 1:
            return self.routing_path[self.cur_addr_index + 1]

    def is_vnf_server(self):
        return self.last_processed_vnf_index + 1 < len(self.vnf_server_addr) and self.get_cur_addr() == \
               self.vnf_server_addr[self.last_processed_vnf_index + 1]

    def get_cur_vnf(self):
        return self.service_chain.get_VNFs[self.last_processed_vnf_index]

    def get_next_required_vnf(self):
        if self.last_processed_vnf_index < len(self.service_chain.get_VNFs()) - 1:
            return self.service_chain.get_VNFs()[self.last_processed_vnf_index + 1]

    def finish_process(self):
        self.last_processed_vnf_index += 1

    def get_size(self):
        return self.size

    def get_src(self):
        return self.src_addr

    def get_dest(self):
        return self.dest_addr

    @staticmethod
    def gen_packet_pool(servers, paths, chains):
        '''
        Randomly generate a packet by specifying its
        1. source/destination addresses,
        2. associated service chain, and
        3. the corresponding routing path.
        :param server_addrs:
        :param chains:
        :return:
        '''
        packets = []
        cnt = 1000
        server_addrs = list(servers.keys())
        for _ in range(cnt):
            size = random.gauss(1024, 400)

            # randomly select source and destination address
            src, dest = random.choice(server_addrs), random.choice(server_addrs)
            # if src == dest:
            #     continue
            p = Packet(size, src, dest, servers)
            p.cur_addr = src

            # randomly associate the packet to a service chain and
            # record all the VNFs of the service chain
            selected_service_chain_index = random.choice(range(len(chains)))
            p.service_chain = chains[selected_service_chain_index]
            vnf_server_addrs = p.service_chain.placement
            p.vnf_server_addr = vnf_server_addrs

            # find the routing path to arrive each VNF serving server along the path.
            cross_server_addrs = [src] + vnf_server_addrs + [dest]
            path = []
            for i in range(len(cross_server_addrs) - 1):
                path.append(find_shortest_path(paths, cross_server_addrs[i], cross_server_addrs[i + 1]))

            # post-processing of the routing path
            # flatten the routing path
            for i in range(len(path) - 1):
                p.routing_path += path[i][:-1]
            p.routing_path += path[-1]

            packets.append(p)

        return packets
