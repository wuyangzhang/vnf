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
import simpy

from core.env import env
from core.virtualNetworkFunction import VirtualNetworkFunction
from conf import configure


types = {'m4.large': (2, 8),
         'm4.xlarge': (4, 16),
         'm4.2xlarge': (8, 32),
         'm4.4xlarge': (16, 64),
         'm4.10xlarge': (40, 160)}

random.seed(4)


class Process:
    def __init__(self, vnf, server, proc_time=0.05):
        self.vnf = vnf
        self.thread = simpy.Resource(env, 1)
        self.buffer = simpy.Store(env)
        self.proc_time = proc_time
        self.server = server

    def put(self, packet):
        self.buffer.put(packet)

    def request(self):
        return self.thread.request()

    def process(self):
        while True:
            with self.request() as req:
                packet = yield self.buffer.get()
                # request one processor
                yield req

                # todo: find the processing time for each VNF
                yield env.timeout(self.proc_time)
                packet.finish_process()

                self.server.out_buffer.put(packet)


class Server:
    def __init__(self, addr, type):
        self.addr = addr
        self.type = type
        self.cpus, self.mem = types[type]
        self.used_cpus, self.used_mem = 0, 0
        self.avail_cpus = self.cpus
        self.avail_mem = self.mem
        self.attached_vnfs = list()

        self.in_buffer = simpy.Store(env)
        self.out_buffer = simpy.Store(env)
        self.env = env

        # each process handles an individual VNF
        self.processes = dict()

        self.links = None

    def run(self):
        env.process(self.in_packet_proc())
        env.process(self.out_packet_proc())
        self.create_vnf_processes()

    def create_vnf_processes(self):
        '''
        Create a process for each assigned VNF
        :return: processes dict
        '''
        for v in self.attached_vnfs:
            p = self.processes[v.id] = Process(v, self)
            env.process(p.process())

    def in_packet_proc(self):
        while True:
            # pull out packets from the queue
            packet = yield self.in_buffer.get()
            packet.update_cur_addr()

            #print('id {}\n last_vnf {}\n routing_path {}\n vnf servers{}\n\n'.format(packet.id, packet.last_processed_vnf_index, packet.routing_path, packet.vnf_server_addr))

            if configure.debug:
                print('Server {} receives the packet {} at {}'.format(self.addr, packet.id, env.now))

            if packet.need_vnf_proc():
                vnf_id = packet.get_next_required_vnf().id
                p = self.processes[vnf_id]
                p.put(packet)

            else:
                self.out_buffer.put(packet)

    def out_packet_proc(self):
        '''
        Process the packet ready to send out to the next hop or to finish the full forwarding.
        :return:
        '''
        while True:
            packet = yield self.out_buffer.get()
            # finish the processing of the packet.

            if configure.debug:
                print('Server {} sends the packet {} at {}'.format(self.addr, packet.id, env.now))

            if packet.is_dest_addr():
                packet.done()
                continue

            # the next VNF locates on the same server.
            # if packet.need_vnf_proc():
            #     vnf_id = packet.get_next_required_vnf().id
            #     p = self.processes[vnf_id]
            #     p.put(packet)
            #     continue

            # forward to the next hop

            cur_addr = packet.get_cur_addr()
            next_hop_addr = packet.get_next_hop_addr()

            if cur_addr == next_hop_addr:
                self.in_buffer.put(packet)
            else:
                link = self.links[(cur_addr, next_hop_addr)]
                link.put(packet)

    def recv_packet(self, packet):
        self.in_buffer.put(packet)

    def attach_vnf(self, vnf: VirtualNetworkFunction):
        '''
        :param vnf: the vnf to be attached
        :return: True if successfully attached, otherwise return False
        '''
        # check demanded resources
        if self.avail_cpus < vnf.CPU or self.avail_mem < vnf.memory:
            return False

        self.attached_vnfs.append(vnf)

        # update available resources
        self.avail_cpus -= vnf.CPU
        self.avail_mem -= vnf.memory
        return True

    def print_avail_resources(self):
        print('server {}: available CPU {}, available mem {}'.format(self.addr, self.avail_cpus, self.avail_mem))

    @staticmethod
    def create_random_server(addr):
        '''
        randomly select a server
        :param addr:
        :return: a server instance
        '''
        seed = random.uniform(0, 1)
        if 0 < seed < 0.2:
            return Server(addr, 'm4.large')
        elif 0.2 < seed < 0.6:
            return Server(addr, 'm4.xlarge')
        elif 0.6 < seed < 0.8:
            return Server(addr, 'm4.2xlarge')
        elif 0.8 < seed < 0.95:
            return Server(addr, 'm4.4xlarge')
        return Server(addr, 'm4.10xlarge')

    @staticmethod
    def create_small_server(addr):
        return Server(addr, 'm4.large')

    @staticmethod
    def create_large_server(addr):
        return Server(addr, 'm4.10xlarge')

    @staticmethod
    def init_servers(nodes, links):
        '''
        Get all the node from the topology and assign a server to it...
        :param nodes:
        :return: a server list
        '''
        servers = {}
        for node in nodes:
            server = Server.create_random_server(node.id)
            server.links = links
            servers[node.id] = server
        return servers
