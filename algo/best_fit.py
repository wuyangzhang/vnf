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

from typing import List

from core.server import Server


def best_fit(servers: List[Server], chain):
    '''
    Allocate a VNF to the server with the most available resources
    :param servers:
    :param chains:
    :return:
    '''

    for v in chain.get_VNFs():
        # sorted servers and find the one with the most available resources
        # use the available CPU num and the available memory as the sorting metrics
        sorted_servers = list({k: v for k, v in sorted(servers.items(), key=lambda item: (
            -item[1].avail_cpus, -item[1].avail_mem))}.keys())
        selected_server = servers[sorted_servers[0]]

        # selected_server.print_avail_resources()
        # print(v)
        # attach the VNF to the selected server
        if not selected_server.attach_vnf(v):
            print('Warning: Not enough available resources to attach VNF {} to server {}\n'.format(v.id,
                                                                                                   selected_server.addr))
            chain.placement = []
            break
        else:
            chain.placement.append(selected_server.addr)
        print('Place vnf {} v to the server {}'.format(v.id, selected_server.addr))
    return chain
