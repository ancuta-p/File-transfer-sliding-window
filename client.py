import socket
import packet
import threading
import time
recv_addr = (socket.gethostname(), 7780)
c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c_socket.bind((socket.gethostname(), 8080))
lock = threading.Lock()
clogfile = open("c_log.txt", 'w+')

N = 4  # window size
TIMEOUT = 10
base = -1
seq_num = 0
last_ack = -1
last_w = -1
packets = []
window = [0 for i in range(N)]
timers = [0 for i in range(N)]  # todo
eoa = False
eot = False

def pkts_to_send(filename):  # packets list
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
    file.close()
    packets.append(b'')  # last packet, empty
    num_packets = len(packets)
    clogfile.write("Total packets: "+ str(num_packets-1))

    
def receive():  # ack thread
    global base
    global seq_num
    global last_ack
    global eoa

    while not eoa:
        pkt, _ = c_socket.recvfrom(8)
        ack, _ = packet.extract(pkt)
        clogfile.write("\ngot ack  " + str(ack))

        if ack >= base:
            lock.acquire()
            window[ack % N] = 0
            timers[ack%N]=0#
            base = ack+1
            last_ack += 1
            lock.release()

        if last_ack == last_w and eot:
            eoa = True


def send():  # send packets
    global last_w
    global seq_num
    global eot
    global eoa

    while not eot:
        next = last_w + 1
        clogfile.write("\nsending packet " + str(next))

        if packet.isempty(packets[next]):
            clogfile.write(" - empty")
            eot = True
        window[next % N] = packets[next]
        timers[next%N]=t.start()#
        c_socket.sendto(packets[next], recv_addr)
        last_w += 1
        seq_num += 1

    while not eoa:
        pass
    clogfile.write("\nclosing client")
    c_socket.close()


pkts_to_send("input.txt")
ack_thread = threading.Thread(target=receive, args=())
ack_thread.start()
send()
