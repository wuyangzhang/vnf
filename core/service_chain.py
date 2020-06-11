import random

import uuid

from .virtualNetworkFunction import VirtualNetworkFunction

class ServiceChain:
    def __init__(self, id, chain):
        self.id = id
        self.chain = chain

    def next_VNF(self, vnf: VirtualNetworkFunction):
        '''
        Find the next VNF in the service chain
        :param vnf: the current reference VNF
        :return: the next VNF in the chain. Return None if the current VNF is the last one or the current VNF does not exist in the chain
        '''
        for i, v in enumerate(self.chain):
            if v == vnf:
                if i == len(self.chain) - 1:
                    return
                return self.chain[i+1]

    def __str__(self):
        s = ''
        for v in self.chain:
            s += v.__str__() + '\n'
        return s

    @staticmethod
    def random_gen():
        '''
        Randomly select 4-8 VNFs and formulate a service chain..
        :return: a composite service chain
        '''

        id = uuid.uuid4()

        # select random total VNF number
        vnf_num = random.randint(4, 9)

        # randomly select x VNFs
        vnfs = [VirtualNetworkFunction.get_random_vnf() for _ in range(vnf_num)]

        # randomly generate a service chain
        random.shuffle(vnfs)

        return ServiceChain(id, vnfs)


if __name__ == '__main__':
    chain = ServiceChain.random_gen()
    print(chain)




