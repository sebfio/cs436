# Assignment 1
### Sebastian Fiorini
### sxfiorin
### 20558540

The purpose of this system is to make an out-of-band control mechanism. This is achieved by connecting to a server on one socket and once some control data is passed sending this information through another socket that is opened to actually transfer this data.

This mechanism is advantageous since we know all the info received on the control channel relates to channel control / sync and the data on the data channel is for consumption / data.

This program is written in python so no compilation is needed.

This program **uses** python3.

To launch the server:
```
python3 tcpserver.py <PORT_NUMBER>
```

To launch the client:
```
python3 tcpclient.py <SERVER_HOSTNAME> <PORT_NUMBER>
```

This can be tested on the following CS undergrad computers:
- ubuntu1604-002.student.cs.uwaterloo.ca
- ubuntu1604-006.student.cs.uwaterloo.ca
- ubuntu1604-008.student.cs.uwaterloo.ca

## NOTE: That if a file that is requested does not exist a blank file is transferred
This was a design choice that was made as specific instruction for files that don't exist was not specified in the assignment.

## Testing
A sample text file can be used. The diff is the compared against the original to show that the file was successfully downloaded.
