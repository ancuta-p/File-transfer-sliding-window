import socket
import packet


def receive(s_socket, filename):
    try:
        file = open(filename, 'wb')
    except IOError:
        print("Error opening file")
        return

    pkt, addr = s_socket.recvfrom(1024)
    seq_num, data = packet.extract(pkt)
    exp_num = 0
    if seq_num == exp_num:
        clogfile.write("sending ack "+ str(exp_num))
        pkt=packet.make(exp_num)
        s_socket.sendto(pkt,(socket.gethostname(),1234))
        file.write(data)
    file.close()

clogfile=open("c_log.txt",'w+')
s_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s_socket.bind((socket.gethostname(),1234))
receive(s_socket,"output.txt")
s_socket.close()




