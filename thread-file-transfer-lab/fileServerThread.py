#!/usr/bin/env python3

import sys, re, os, socket
from threading import Thread;
from encapFramedSock import EncapFramedSock

def main():

    host,port = parseArguments()

    if host is None:
        print("Default IP address being used:127.0.0.1")
        host = "127.0.0.1"
    if port is None:
        print("Default port being used:50000")
        port = 50000

    
    addrFamily = socket.AF_INET
    socktype = socket.SOCK_STREAM
    addrPort = (host,port)

    serverSocket = socket.socket(addrFamily,socktype)

    if serverSocket is None:
        print('could not open socket')
        sys.exit(1)

    serverSocket.bind(addrPort)
    serverSocket.listen(5)
    print("Listening on: ",addrPort)

    while True:
        sockAddr = serverSocket.accept()
        server = Server(sockAddr)
        server.start()

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            fileName = self.fsock.receive()
            try:
                newFile = open(fileName,"x")
            except :
                print("File already exists!")
                sys.exit(1)
            received = self.fsock.receive()
            if(received is None):
                os.remove(fileName)
                print("Something went wrong, the file could not be fully recieved")
                sys.exit(1)
            while received != b'DoneSending':
                newFile.write(received.decode())
                received = self.fsock.receive()
                if(received is None):
                    os.remove(fileName)
                    print("Something went wrong, the file could not be fully recieved")
                    sys.exit(1)
            print("Finished receiving")
            newFile.close()
            return          # exit

def parseArguments():
    if(len(sys.argv) == 1):
        return None,None
    if(len(sys.argv) == 2):
        try:
            host, port = re.split(":",sys.argv[1])
            port = int(port)
            return host,port
        except:
            port = sys.argv[1]
            port = int(port)
            return None,port
    else:
        print("Too many arguments!")
        sys.exit(1)

if __name__ == '__main__':
    main()
