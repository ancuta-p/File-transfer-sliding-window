def make(seq_num, data=b''):
    seq_bytes=seq_num.to_bytes(4, byteorder = 'little',signed = True)
    return seq_bytes + data


def extract(packet):
    seq_num=int.from_bytes(packet[0:4],byteorder = 'little',signed = True)
    return seq_num, packet[4:]


def isempty(packet):  # last packet
    if packet[4:] == b'':
        return True
    return False

