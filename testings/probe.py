from socket import socket as S
from struct import pack
from time import sleep

def go():
    print "going"
    s = S(2,1)
    s.connect(("127.0.0.1", 7000))
    print "connected"
    msg1 = '{"ip": "1.2.3.4"}'
    s.send(pack("!h", len(msg1)) + msg1)
    print ("sending ID")
    sleep(0.001)
    print(s.recv(1000))
    while 1:
        msg = raw_input("MSG: ")
        s.send(pack("!h", len(msg)) + msg)
        print(s.recv(1024))

go()
