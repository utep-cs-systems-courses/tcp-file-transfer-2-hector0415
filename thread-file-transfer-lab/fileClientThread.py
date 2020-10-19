#!/usr/bin/env python3

import os, re, socket, sys
from encapFramedSock import EncapFramedSock

def main():
    arguments = parseArguments()

    addrFamily = socket.AF_INET
    socktype = socket.SOCK_STREAM
    
    addrPort = (arguments["host"], arguments["port"])

    clientSocket = socket.socket(addrFamily,socktype)

    if clientSocket is None:
        print('could not open socket')
        sys.exit(1)

    clientSocket.connect(addrPort)

    fsock = EncapFramedSock((clientSocket,addrPort))

    sendFile(fsock,arguments["source"],arguments["destination"])
    transferResult = fsock.receive()
    transferResult = transferResult.decode()
    print(transferResult)


def sendFile(fsock,source,destination):
    try:
        fileSend = open(source,"r")
    except:
        print("Could not open source file")
        sys.exit(1)
    fsock.send(destination.encode())
    for line in fileSend:
        fsock.send(line.encode())
    fsock.send(b'DoneSendingFileFromClient')

def parseArguments():
    arguments ={}
    if(len(sys.argv) <= 2):
        print("Too few arguments!\nNeed <ip address:port> <sourceFileName> [destinationFileName]")
        sys.exit(1)
    elif((len(sys.argv) == 3) or (len(sys.argv) == 4)):
        try:
            host, port = re.split(":",sys.argv[1])
            port = int(port)
            arguments["host"] = host
            arguments["port"] = port
        except:
            print("Can't parse server:port from '%s'" % sys.argv[1])
            sys.exit(1)
        try:
            fileName,ext = re.split('\.',sys.argv[2])
            arguments["source"] = sys.argv[2]
        except:
            print("Cannot find valid extension in source file argument")
            sys.exit(1)
        if(len(sys.argv) == 4):
            try:
                fileName,ext = re.split('\.',sys.argv[3])
                arguments["destination"] = sys.argv[3]
            except:
                print("Cannot find valid extension in destination file argument")
                sys.exit(1)
        else:
            arguments["destination"] = sys.argv[2]
    else:
        print("Too many arguments!\nNeed <ip address:port> <sourceFileName> [destinationFileName]")
        sys.exit(1)
    return arguments

if __name__ == '__main__':
    main()
