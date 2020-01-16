import socket
import packet
import random
import logging as log

send_addr = (socket.gethostname(), 8080)
s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_socket.bind((socket.gethostname(), 7780))
log.basicConfig(filename='slog.out', filemode='w', level=log.DEBUG, datefmt='%d-%m-%Y %H:%M:%S', format='%(asctime)s: %(message)s')
PROB = 0.30  # pkt prob loss


def receive(filename="output.out"):
    try:
        file = open(filename, 'wb')
    except IOError:
        log.error("Error opening file")
        return
    exp_num = 0
    while True:
        pkt, addr = s_socket.recvfrom(1024)
        seq_num, data = packet.extract(pkt)
        if packet.isempty(pkt) and seq_num == exp_num :
            log.info("closing server")
            s_socket.close()
            break
      
        if seq_num == exp_num:
            if PROB > random.random():
                log.info("packet " + str(exp_num) + " lost")
                continue
            log.info("got packet " + str(exp_num)+", sending ack")
            pkt = packet.make(exp_num)
            s_socket.sendto(pkt, addr)
            file.write(data)
            exp_num += 1
        elif seq_num < exp_num:
            log.info("seq, exp:  " + str(seq_num) + ", " + str(exp_num))
            log.info("sending ack " + str(seq_num))
            pkt = packet.make(seq_num)
            s_socket.sendto(pkt, addr)
            exp_num = seq_num+1
        else:
            log.info("seq, exp:  " + str(seq_num) + ", " + str(exp_num))
            
    file.close()
    
    
#receive("output.txt")





