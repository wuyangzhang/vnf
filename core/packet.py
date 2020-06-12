import random
import numpy as np

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
    def gen_packet(server_addrs, chains):
        '''
        Randomly generate a packet by specifying its source/destination addresses and associated service chain.
        :param server_addrs:
        :param chains:
        :return:
        '''
        size = np.random.poisson(1024, 1)[0]
        src, dest = random.choice(server_addrs), random.choice(server_addrs)
        return Packet(size, src, dest)
