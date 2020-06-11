class Link:
    def __init__(self, from_node, to_node, bw):
        self.from_node = from_node
        self.to_node = to_node
        self.bandwidth = bw # Mbps


    def get_bw(self):
        return self.bandwidth

    def set_bw(self, val):
        self.bandwidth = val
