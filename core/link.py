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

import simpy

from core.env import env


class Link:
    def __init__(self, from_node, to_node, bw, latency):
        self.from_node = from_node
        self.to_node = to_node
        self.bandwidth = bw  # Mbps
        self.propagation_latency = latency  # ms propagation latency
        # self.queue = simpy.Store(env)
        self.env = env
        self.forwarder = simpy.Resource(env, 1)
        self.buffer = simpy.Store(env)

    def run(self):
        while True:
            with self.forwarder.request() as req:
                packet = yield self.buffer.get()

                yield req

                # forwarding the packet. KB / MB
                forward_time = packet.get_size() / self.bandwidth / 1000
                yield env.timeout(forward_time)

                # print('link from {} to {} forwards the packet {} at time {}'.format(self.from_node.id, self.to_node.id,
                #                                                                     packet.id, env.now))

                env.process(packet.forward(self.propagation_latency))

    def put(self, packet):
        self.buffer.put(packet)

    def get_bw(self):
        return self.bandwidth

    def set_bw(self, val):
        self.bandwidth = val

    def __str__(self):
        return 'link from {} to {}'.format(self.from_node.id, self.to_node.id)

    #
    # def get(self):
    #     return self.queue.get()

    # def latency(self, packet):
    #     yield self.env.timeout(self.latency)
    #     self.store.put(packet)
