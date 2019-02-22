from socket import *
import sys
from file_over_network import *

def main(serverName, serverPort):
    """ Main program for running through the two step sequence to transfer files over between the two computers """
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    
    command = input("Request and filename: ")
    
    if request == "EXIT":
        print("User exit received.")
        # TODO: Do we need to shut down???
        clientSocket.close()
        exit(0)

    action = ""
    filename = ""
    
    clientSocket.send(command.encode())
    
    request_valid = clientSocket.recv(1024).decode()
    if request_valid != "OK": 
        sys.stderr.write("Server did not correctly understand request.\n")
        clientSocket.close()
        exit(1)

    # NOTE: We know user properly entered request in the form <HTTP VERB> : <FILENAME>
    #   since the server responded with 'OK' hence no need for try/except here
    action, filename = command.split()
    
    # Stage 2 socket initialization, for stage 2, the client becomes the server
    s2Sock = socket(AF_INET, SOCK_STREAM)
    # Let OS pick us a free port
    s2Sock.bind(('', 0))
    s2SockPort        = s2Sock.getsockname()[1]
    s2SockHostName    = socket.gethostname()
    s2Info = str(s2SockPort) + "," + s2SockHostName

    clientSocket.send(s2Info.encode())
    clientSocket.close()
    
    if action == "GET":
        get_cmd(filename, s2Sock, 1024)
    elif action == "PUT":
        put_cmd(filename, s2Sock, 1024)
    else:
        # Unknown action
        sys.stderr.write("Got an invalid action, need PUT or GET, got: %s\n" % action)
        s2Sock.close()
        exit(1)

    s2Sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("%s needs 3 arguments to run!\n" % sys.argv[0])
        exit(1)
    
    serverName = sys.argv[1]
    serverPort = sys.argv[2] 

    main(serverName, serverPort)
