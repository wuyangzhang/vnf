import random
import numpy as np
from .routing import find_shortest_path
import simpy

class Packet:
    def __init__(self, size, src, dest):
        self.size = size # Byte
        self.src = src
        self.dest = dest
        self.service_chain = None
        self.routing_path = []

    def get_size(self):
        return self.size

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    @staticmethod
    def gen_packet_pool(server_addrs, chains, paths):
        '''
        Randomly generate a packet by specifying its source/destination addresses and associated service chain.
        :param server_addrs:
        :param chains:
        :return:
        '''
        packets = []
        routing_path = []
        cnt = 1000
        for _ in range(cnt):
            size = np.random.poisson(1024, cnt)[0]
            src, dest = random.choice(server_addrs), random.choice(server_addrs)
            packets.append(Packet(size, src, dest))

            path = find_shortest_path(paths, src, dest)
            routing_path.append(path)

        return packets

    @staticmethod
    def gen_packet(env, packets_pool, out_pipe):
        while True:
            yield env.timeout(1)
            out_pipe.put(random.choice(packets_pool))

