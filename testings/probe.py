from socket import socket as S
def go():
    s = S(2,1)
    s.connect(("localhost", 7000))
    s.send('{"ip":"1.1.1.1"}')
    print(s.recv(1000))
    s.send('this is a really long string')
    print(s.recv(1000))

go()