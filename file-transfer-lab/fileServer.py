import os, re, socket, sys, time

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("localhost", 50001))
    
    serverSocket.listen(1)

    conn, addr = serverSocket.accept()
    print("connected") #Used for debugging
    fileName = receive(conn)
    found = os.path.exists(fileName)

    if found: #need to fix appending copy to the name of the file
        print("A file with that name already exists, making copy")
        Contents = receive(conn)
        name,ext = re.split('.',fileName,1)
        name = name+"_copy"
        newFile = open(name+ext,'x')
        newFile.write(Contents)
        newFile.close()
    else:
        Contents = receive(conn)
        newFile = open(fileName,'x')
        newFile.write(Contents)
        newFile.close()
    

    fileTR = 0

def receive(conn):
    received = conn.recv(64).decode()
    size,msg = re.split(':',received,1)
    size = int(size) - 1

    while len(msg) < size:
        msg = msg + conn.recv(64).decode()
        
    return msg

if __name__ == '__main__':
    main()