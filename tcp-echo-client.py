#!/usr/bin/python
import socket, io, sys

if len(sys.argv) < 2:
    print "usage: %s host port" % (sys.argv[0])
    sys.exit(-1)

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket()
s.connect((host,port))

try:
    s.send("hello there\n")
    data = s.recv(1024)
    print data
finally:
    s.close()
