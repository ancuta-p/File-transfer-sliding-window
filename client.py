import socket
import packet
import threading
import time
recv_addr = (socket.gethostname(), 7780)
c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c_socket.bind((socket.gethostname(), 8080))
lock = threading.Lock()
clogfile = open("c_log.txt", 'w+')

def pkts_to_send(c_socket,filename):  # packets list
    try:
        file=open(filename,'rb')
    except IOError:
        clogfile.write("error opening file")
        return
    i = 0
    while True:
        data = file.readline()
        if not data:
            break
        packets.append(packet.make(i, data))
        i += 1
    packets.append(b'')  # last packet, empty
    num_packets = len(packets)
    clogfile.write("Total packets: "+ str(num_packets-1))

    c_socket.sendto(packets[idx],(socket.gethostname(),1234))
    file.close()


pkts_to_send("input.txt")
#ack_thread = threading.Thread(target=receive, args=())
#ack_thread.start()

c_socket.close()
