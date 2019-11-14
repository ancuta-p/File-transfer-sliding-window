import socket
import packet

def send(c_socket,filename):
    try:
        file=open(filename,'rb')
    except IOError:
        print("Error opening file")
        return

    seq_num=0
    idx=0
    packets=[]
    while True:
        data = file.readline()
        if not data:
            break
        packets.append(packet.make(seq_num, data))
        seq_num += 1
    num_packets = len(packets)
    slogfile.write("Total packets: "+ str(num_packets))

    c_socket.sendto(packets[idx],(socket.gethostname(),1234))
    file.close()


slogfile=open("s_log.txt",'w+')
c_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
send(c_socket,"input.txt")

c_socket.close()