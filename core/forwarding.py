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

from core.env import env

def forward_packet(packet, servers, links):
    '''
    recursively call forward_packet until the packet arrives at the destination
    :param packet:
    :param servers:
    :param links:
    :return:
    '''

    server_addr = packet.get_cur_addr()
    cur_server = servers[server_addr]

    if packet.is_dest_addr():
        if packet.is_vnf_server():
            cur_server.put(packet)
            cur_server.get_processed_packet()
        return

    if packet.is_vnf_server():
        cur_server.put(packet)
        cur_server.get_processed_packet()

    next_hop = packet.get_next_hop_addr()
    cur_addr = packet.get_cur_addr()

    # get the link and forward.
    link = links(cur_addr, next_hop)
    link.put(packet)

    # forward to the next server.
    packet = link.get_forwarded_packet()

    # update packet address
    packet.forward()

    return forward_packet(packet, servers, links)