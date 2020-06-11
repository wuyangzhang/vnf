
class Packet:
    def __init__(self, id, size, src, dest):
        self.id = id
        self.size = size
        self.src = src
        self.dest = dest

    def get_size(self):
        return self.size

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    @staticmethod
    def gen_packet():
        return Packet(10, 10, 10, 10)
