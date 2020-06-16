import random

import uuid

class VirtualNetworkFunction:
    def __init__(self, name, cpu, mem, thr):
        self.id = uuid.uuid4()
        self.name = name

        self.CPU = cpu # count
        self.memory = mem  # GB
        self.throughput = thr # Mbps
        self.attached_server = None

    def __str__(self):
        return 'id: {}, requested CPU num: {}, requested memory: {} GB, throughput: {} Mbps'.format(self.name, self.CPU, self.memory, self.throughput)

    def attach_server(self, server):
        self.attached_server = server

    @staticmethod
    def get_random_vnf():
        return random.choice([VirtualNetworkFunction.vnf1(),
                              VirtualNetworkFunction.vnf2(),
                              VirtualNetworkFunction.vnf3(),
                              VirtualNetworkFunction.vnf4(),
                              VirtualNetworkFunction.vnf5(),
                              VirtualNetworkFunction.vnf6(),
                              VirtualNetworkFunction.vnf7(),
                              VirtualNetworkFunction.vnf8()])

    @staticmethod
    def vnf1():
        return VirtualNetworkFunction('firewall_small', 4, 2, 100)

    @staticmethod
    def vnf2():
        return VirtualNetworkFunction('firewall_normal', 4, 8, 200)

    @staticmethod
    def vnf3():
        return VirtualNetworkFunction('firewall_large', 4, 8, 400)

    @staticmethod
    def vnf4():
        return VirtualNetworkFunction('IDS', 4, 6, 80)

    @staticmethod
    def vnf5():
        return VirtualNetworkFunction('IPSec_normal', 4, 4, 268)

    @staticmethod
    def vnf6():
        return VirtualNetworkFunction('IPSec_large', 4, 8, 580)

    @staticmethod
    def vnf7():
        return VirtualNetworkFunction('wan_opt_normal', 2, 2, 10)

    @staticmethod
    def vnf8():
        return VirtualNetworkFunction('wan_opt_large', 2, 4, 50)


if __name__ == '__main__':
    vnf = VirtualNetworkFunction.get_random_vnf()
    print(vnf)