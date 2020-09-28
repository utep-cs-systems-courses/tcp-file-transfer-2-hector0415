import os, re, socket, sys

def main():
    fileTS = None

    while fileTS is None:
        print("Enter Name of file, or type \'exit\' to terminate")
        action = input("$ ")
        if action.lower() == "exit": #if exit entered, close program
            sys.exit(0)
        else:
            try:
                fileTS = open(action)
            except IOError:
                pass
                print("Could not find file, please try again")
            
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("localhost", 50001))

    firstSend = str(len(action))+':'+action
    clientSocket.sendall(firstSend.encode()) #Send file name first before sending actual file

    print("Sending file to server")
    send(clientSocket,fileTS)

def send(sock,file):
    sizeOfFile = os.path.getsize(file.name)
    send = str(sizeOfFile)+':'+file.read()
    sock.sendall(send.encode())

    line = file.read()
    while line != '':
        sock.sendall(line.encode())
        line = file.read()
    print("done sending message")
    



if __name__ == '__main__':
    main()