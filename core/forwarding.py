'''
input: packet, routing path, servers, links, cur_pos
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