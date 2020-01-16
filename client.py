import socket
import packet
import threading
import time
import random
import logging as log

recv_addr = (socket.gethostname(), 7780)
c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c_socket.bind((socket.gethostname(), 8080))
lock = threading.Lock()
ack_thread = threading.Thread(target=receive, args=())
log.basicConfig(filename='clog.out', filemode='w', level=log.DEBUG, datefmt='%d-%m-%Y %H:%M:%S', format='%(asctime)s: %(message)s')

N = 4  # window size
TIMEOUT = 2
base = 0
seq_num = 0
last_ack = -1
last_w = -1
packets = []
window = []
timers = []
total_packets = 0
eoa = False  # end of acks
eot = False  # end of transmission

def pkts_to_send(filename):  # packets list
    global total_packets
    global packets
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
    total_packets = len(packets)

    
def receive():  # ack thread
    global base
    global timers
    global seq_num
    global last_ack
    global eoa

    while not eoa:
        pkt, _ = c_socket.recvfrom(8)
        ack, _ = packet.extract(pkt)
        
        if PROB < random.random():
            if ack == last_ack + 1:
                lock.acquire()
                log.info("received ack " + str(ack))
            window[ack % N] = None
            if timers[ack % N] != 0:
                timers[ack % N].cancel()
                timers[ack % N] = 0           
            
            base = base+1
            last_ack += 1
            lock.release()
                else:
        else:
            log.info("ack " + str(ack) + " lost")

        if last_ack == last_w and eot:
            eoa = True


def send():  # send packets
    global last_w
    global timers
    global seq_num
    global eot
    global eoa

    log.info("total packets: " + str(total_packets))
    log.info("starting transmission...")
    while last_w < total_packets:
        if last_w >= base+N:  # window is full
            continue
        next = last_w
        log.info("sending packet " + str(next))

        if next < N:
            window.append(packets[next])
            t = threading.Timer(TIMEOUT, timeout)
            t.start()
            timers.append(t)
        else:
            window[next % N] = packets[next]
            t = threading.Timer(TIMEOUT, timeout)
            t.start()
            timers[next % N] = t

        time.sleep(1)    
        c_socket.sendto(packets[next], recv_addr)
        last_w += 1
        seq_num += 1
        
    eot = True
    while not eoa:
        pass
    log.info("end of transmission")
    c_socket.sendto(packet.make(seq_num, b''), recv_addr)
    clogfile.write("\nclosing client")
    c_socket.close()


#pkts_to_send("Mr. Coyote Meets Mr. Snail.txt")
#ack_thread.start()
#send()
