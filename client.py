import socket, sys

HOST, PORT = "52.206.182.231", 8080

# create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # connect to server 
    sock.connect((HOST, PORT))

    # send data
    sock.sendall(bytes("@@090-31513450010F21629200000000000020F7993100000000000020190211162029082996941608299617740BNEWMOVEMENT031SPOT Trace has detected that the asset has moved.03291010F0090000000000000", encoding='UTF-8'))
    # sock.sendall(bytes("@@090-31513450010F21520100000000000020F7993140000000000020190131165755082996977108299694160FUNLIMITED-TRACK00003358010F1210000000000000", encoding='UTF-8'))

    # receive data back from the server
    received = str(sock.recv(1024))
finally:
    # shut down
    sock.close()

print("Sent:     {}".format(data))
print("Received: {}".format(received))