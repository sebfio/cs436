from socket import *
import sys
from file_over_network import *

def main(serverName, serverPort):
    """ Main program for running through the two step sequence to transfer files over between the two computers """
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    command = ""
    while command == "":
        # Loop in case a user hits enter key wihtout entering text
        command = input("Request and filename: ")
    
    if command == "EXIT" or command == "exit":
        print("User exit received.")
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
    action = action.upper()
    
    # Stage 2 socket initialization, for stage 2, the client becomes the server
    s2Sock = socket(AF_INET, SOCK_STREAM)
    # Let OS pick us a free port. This is what's done when you pass a port number 0 in python
    s2Sock.bind(('', 0))
    s2SockPort        = s2Sock.getsockname()[1]
    # Get the hostname of the device. Alternatively, you could read 
    # /etc/hostname on a linux machine
    s2SockHostName    = gethostname()
    # Pack the port and hostname into a string to send over. This is probably
    # the easiest way to send it over
    s2Info = str(s2SockPort) + "," + s2SockHostName
    s2Sock.listen(1)

    # Control mechanism pipe no longer needed since the server responded with 'OK'.
    # We presume the server to agree with the connection protocol that is defined and 
    # connect to us now in order to transfer the file.
    clientSocket.send(s2Info.encode())
    clientSocket.close()
    
    c2Sock, addr = s2Sock.accept()
    if action == "GET":
        get_cmd(filename, c2Sock, 1024)
        print ("Got file %s from server." % filename)
    elif action == "PUT":
        put_cmd(filename, c2Sock, 1024)
        print ("Put file %s to server." % filename)
    else:
        # Unknown action. This is for redundancy sake as the server _should not_ respond 'OK'
        # on an invalid request.
        sys.stderr.write("Got an invalid action, need PUT or GET, got: %s\n" % action)
        s2Sock.close()
        exit(1)

    s2Sock.close()

if __name__ == "__main__":
    # Dont run if server hostname and server port not specified
    if len(sys.argv) != 3:
        sys.stderr.write("%s needs 3 arguments to run!\n" % sys.argv[0])
        exit(1)
    
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

    main(serverName, serverPort)
