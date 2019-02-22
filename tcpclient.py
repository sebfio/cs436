from socket import *
import sys
from file_over_network import *

def main(serverName, serverPort):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    
    clientSocket.connect((serverName, serverPort))
    
    command = input("Request and filename: ")
    
    clientSocket.send(command.encode())
    modifiedSentence = clientSocket.recv(1024)
    print('From Sever: ', modifiedSentence.decode())
    clientSocket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("%s needs 3 arguments to run!\n" % sys.argv[0])
        exit(1)
    
    serverName = sys.argv[1]
    serverPort = sys.argv[2] 

    main(serverName, serverPort)
