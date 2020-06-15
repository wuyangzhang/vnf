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

from .virtualNetworkFunction import VirtualNetworkFunction


class ServiceChain:
    def __init__(self, id, vnfs):
        self.id = id
        self.vnfs = vnfs # contained VNFs
        self.placement = [] # VNF server placement

    @staticmethod
    def random_gen(min_vnf_num=4, max_vnf_num=9):
        '''
        Randomly select 4-8 VNFs and formulate a service chain.
        :return: a composite service chain
        '''

        id = uuid.uuid4()

        # select random total VNF number
        contained_vnf_num = random.randint(min_vnf_num, max_vnf_num)

        # randomly select x VNFs
        vnfs = [VirtualNetworkFunction.get_random_vnf() for _ in range(contained_vnf_num)]

        # randomly generate a service chain
        # todo: consider, now it is a line of VNFs but not a graph
        random.shuffle(vnfs)

        return ServiceChain(id, vnfs)

    def next_VNF(self, vnf: VirtualNetworkFunction):
        '''
        Find the next VNF in the service chain
        :param vnf: the current reference VNF
        :return: the next VNF in the chain. Return None if the current VNF is the last one or the current VNF does not exist in the chain
        '''
        for i, v in enumerate(self.vnfs):
            if v == vnf:
                if i == len(self.vnfs) - 1:
                    return
                return self.vnfs[i + 1]

    def get_VNFs(self):
        return self.vnfs


    def __str__(self):
        s = ''
        for v in self.vnfs:
            s += v.__str__() + '\n'
        return s

if __name__ == '__main__':
    chain = ServiceChain.random_gen()
    print(chain)
