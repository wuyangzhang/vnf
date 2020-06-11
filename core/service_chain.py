import random

import uuid

from vnf import VNF

class ServiceChain:
    def __init__(self, id):
        self.id = id
        self.vnf_graph = None

    @staticmethod
    def random_gen():
        '''
        random fetch k VNFs and formulate a graph..
        :return:
        '''

        id = uuid.uuid4()

        # select random total VNF number
        vnf_num = random.randint(4, 8)
        vnfs = [VNF.get_random_vnf() for _ in range(vnf_num)]






