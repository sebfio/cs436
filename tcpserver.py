from socket import *
import sys
from file_over_network import *

def main(serverPort):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    
    print('Server is ready to receive')
    
    while True:
        connectionSocket, addr = serverSocket.accept()
    
        # Act in a case insensitive manner
        request = connectionSocket.recv(1024).decode()
        
        if len(request) == 0:
            continue

        action = ""
        filename = ""
        
        # Try and get the action and filename to operate on
        try:
            action, filename = request.split()
            # only uppercase the 'action' -> ie "GET" "PUT" to halve the amount of condition checks
            action = action.upper()
            if action != "GET" and action != "PUT":
                raise
        except:
            # failed to get a valid request
            sys.stderr.write("Didn't get a valid request, got: %s\n" % request)
            # NOTE: The client will see a connection termination without getting a "OK"
            # so it will understand the user input was not valid
            connectionSocket.close()
            continue

        connectionSocket.send("OK".encode())

        # Get the <r_port>, <client_address>
        # TODO: What do we do if client sends junk port and addr over?
        request = connectionSocket.recv(1024).decode()
        # Done with stage 1 content
        connectionSocket.close()

        # Wont serialize this, instead just send over as a comma separated string
        # NOTE: "s2" prefix for stage 2 stuff
        s2Port, s2Addr = request.split(",")
        s2Port = int(s2Port)
        
        s2Sock = socket(AF_INET, SOCK_STREAM)
    
        s2Sock.connect((s2Addr, s2Port))
        
        # TODO: GET/PUT stuff
        # End of agreement stage
        if action == "GET":
            # send the file over
            # NOTE: Since this is the server the action is reverse of what command was received
            put_cmd(filename, s2Sock, 1024)
            print ("Sent file %s to client." % filename)
        elif action == "PUT":
            # recv the file
            get_cmd(filename, s2Sock, 1024)
            print ("Got file %s from client." % filename)
        else:
            # Unknown action, note this is for redundancy sake
            sys.stderr.write("Got an invalid action, need PUT or GET, got: %s\n" % action)
            s2Sock.close()
            exit(1)

        s2Sock.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("%s needs 2 arguments to run!\n" % sys.argv[0])
        exit(1)

    serverPort = int(sys.argv[1]) 

    main(serverPort)
