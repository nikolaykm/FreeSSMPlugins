import time
import os
import socket
import sys
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024

isConnected=False
while not isConnected:
    isConnected=False
    try:
        print >>sys.stderr, '\n Trying to connect to IP: %s, Port: %s' %(TCP_IP,TCP_PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
        isConnected=True
    except:
        print >>sys.stderr, '\n Unable to connect!'
        isConnected=False
        time.sleep(0.5)

f = open('stats-'+str(time.time()), 'w')

curList = []
while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data = sock.recv(BUFFER_SIZE)
    print >>sys.stderr, 'received %s bytes' % (len(data))
    print >>sys.stderr, data
    
    if data and len(data) > 4:
        data = data[4:]
        ds = data.split(",")
        print ds
        curList.append(ds[0]);
        if (ds[4] == "3"):
            f.write(curList[0] + "," + curList[1] + "," + curList[2] + "," + curList[3] + "," + str(time.time()) + "\n")
            f.flush()
            curList = []

