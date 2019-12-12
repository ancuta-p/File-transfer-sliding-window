import socket
import packet

send_addr = (socket.gethostname(), 8080)
s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_socket.bind((socket.gethostname(), 7780))
slogfile = open("s_log.txt", 'w+')


def receive(filename):
    try:
        file = open(filename, 'wb')
    except IOError:
        print("Error opening file")
        return
    exp_num = 0
    while True:
        pkt, addr = s_socket.recvfrom(1024)
        if packet.isempty(pkt):
            slogfile.write("\nclosing server")
            s_socket.close()
            break
        seq_num, data = packet.extract(pkt)

        if seq_num == exp_num:
            slogfile.write("\ngot packet " + str(exp_num))
            slogfile.write("\nsending ack " + str(exp_num))
            pkt = packet.make(exp_num)
            s_socket.sendto(pkt, addr)
            file.write(data)
            exp_num += 1
        else:
            # slogfile.write("\nseq, exp  " + str(seq_num) + str(exp_num))
            slogfile.write("\nsending ack " + str(exp_num-1))
            pkt = packet.make(exp_num-1)
            s_socket.sendto(pkt, addr)
    file.close()
    
    
receive("output.txt")





