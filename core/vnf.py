import random

class VNF:
    def __init__(self, id, mem, cpu, thr):
        self.id = id
        self.memory = mem # GB
        self.CPU = cpu # count
        self.throughput = thr # Mbps

    def __str__(self):
        return 'id: {}, requested CPU num: {}, requested memory: {} GB, throughput: {} Mbps'.format(self.id, self.CPU, self.memory, self.throughput)

    @staticmethod
    def get_random_vnf():
        return random.choice([VNF.vnf1(),
                              VNF.vnf2(),
                              VNF.vnf3(),
                              VNF.vnf4(),
                              VNF.vnf5(),
                              VNF.vnf6(),
                              VNF.vnf7(),
                              VNF.vnf8()])

    @staticmethod
    def vnf1():
        return VNF('firewall_small', 4, 2, 100)

    @staticmethod
    def vnf2():
        return VNF('firewall_normal', 4, 8, 200)

    @staticmethod
    def vnf3():
        return VNF('firewall_large', 4, 8, 400)

    @staticmethod
    def vnf4():
        return VNF('IDS', 4, 6, 80)

    @staticmethod
    def vnf5():
        return VNF('IPSec_normal', 4, 4, 268)

    @staticmethod
    def vnf6():
        return VNF('IPSec_large', 4, 8, 580)

    @staticmethod
    def vnf7():
        return VNF('wan_opt_normal', 2, 2, 10)

    @staticmethod
    def vnf8():
        return VNF('wan_opt_large', 2, 4, 50)


if __name__ == '__main__':
    vnf = VNF.get_random_vnf()
    print(vnf)