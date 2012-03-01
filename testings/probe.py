from socket import socket as S
from struct import pack
def go():
    print "going"
    s = S(2,1)
    s.connect(("localhost", 7000))
    print "connected"
    msg1 = '{"ip": "1.1.1.1"}'
    s.send(pack("!h", len(msg1)) + msg1)
    print ("sending ID")
    print(s.recv(1000))
    while 1:
        msg = raw_input("MSG: ")
        s.send(pack("!h", len(msg)) + msg)
        print(s.recv(1024))

go()
