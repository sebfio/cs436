from socket import *
import sys
from file_over_network import *

def main(serverPort):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    serverSocket.bind(('', serverPort))
    
    serverSocket.listen(1)
    
    print('The server is ready to receive')
    
    while True:
    	connectionSocket, addr = serverSocket.accept()
    
    	request = connectionSocket.recv(1024).decode()

        if request == "EXIT":
            print("User exit received.")
    	    connectionSocket.close()
            exit(0)

        action = ""
        filename = ""
        
        # Try and get the action and filename to operate on
        try:
            action, filename = request.split()
            action = action.upper()
            filename = filename.upper() 
        except:
            # failed to get a valid request
            sys.stderr.write("Didn't get a valid request, got: %s\n" % request)
    	    connectionSocket.close()
            break

    	connectionSocket.send("OK".encode())

    	# Get the <r_port>, <client_address>
        # TODO: What do we do if client sends junk port and addr over?
        request = connectionSocket.recv(1024).decode()
        # Done with stage 1 content
    	connectionSocket.close()

        # Wont serialize this, instead just send over as a comma separated string
        # NOTE: "s2" prefix for stage 2 stuff
        s2port, sAddr = request.split(",")
        
        s2Sock = socket(AF_INET, SOCK_STREAM)
    
        s2Sock.connect((s2Addr, s2Port))
        
        # TODO: GET/PUT stuff
        # End of agreement stage
        if action == "GET":
            # send the file over
            # NOTE: Since this is the server the action is reverse of what command was received
            put_cmd(filename, s2Sock, 1024)
        elif action == "PUT":
            # recv the file
            get_cmd(filename, s2Sock, 1024)
        else:
            # Unknown action
            sys.stderr.write("Got an invalid action, need PUT or GET, got: %s\n" % action)
            s2Sock.close()
            exit(1)

        s2Sock.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("%s needs 2 arguments to run!\n" % sys.argv[0])
        exit(1)

    serverPort = sys.argv[1] 

    main(serverPort)
