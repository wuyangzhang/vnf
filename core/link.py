import simpy

from core.env import env

class Link:
    def __init__(self, from_node, to_node, bw, latency):
        self.from_node = from_node
        self.to_node = to_node
        self.bandwidth = bw # Mbps
        self.latency = latency
        self.store = simpy.Store(env)
        self.env = env

    def get_bw(self):
        return self.bandwidth

    def set_bw(self, val):
        self.bandwidth = val

    def latency(self, packet):
        yield self.env.timeout(self.latency)
        self.store.put(packet)

    def put(self, packet):
        self.env.process(self.latency(packet))

    def get(self):
        return self.store.get()

    def get_forwarded_packet(self):
        while True:
            packet = yield self.get()
            return packet