import random
from core.virtualNetworkFunction import VirtualNetworkFunction

types = {'m4.large': (2, 8),
         'm4.xlarge': (4, 16),
         'm4.2xlarge': (8, 32),
         'm4.4xlarge': (16, 64),
         'm4.10xlarge': (40, 160)}


class Server:
    def __init__(self, addr, type):
        self.addr = addr
        self.type = type
        self.cpus, self.mem = types[type]
        self.used_cpus, self.used_mem = 0, 0
        self.avail_cpus = self.cpus
        self.avail_mem = self.mem
        self.attached_vnfs = list()

    def attach_vnf(self, vnf: VirtualNetworkFunction):
        '''

        :param vnf: the vnf to be attached
        :return: True if successfully attached, otherwise return False
        '''
        self.attached_vnfs.append(vnf)

        # update available resources

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
    def init_servers(nodes):
        '''
        Get all the node from the topology and assign a server to it...
        :param nodes:
        :return: a server list
        '''
        servers = {}
        for node in nodes:
            server = Server.create_random_server(node.id)
            servers[node.id] = server
        return servers




