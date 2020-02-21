import socket
import sys

#* .AF_INET corresponds to IPV4
#* SOCK_STREAM corresponds to TCP

# def print2DArray(array):
#     for row in array:
#         print '[',
#         for item in row:
#             print item,
#         print ']'
#         print("")

def convertFileToArray(file_path):
    f = open(file_path, "r")

    result = []

    contents = f.readlines()
    for line in contents:        
        line = line.rstrip('\n')
        line = line.rstrip('\r')

        # split line on space
        splitString = line.split()        

        result.append(splitString)
                
    return result    

def getDomainFromTable(dns_table, client_domain):
    for row in dns_table:        
        hostname = row[0]
        ip_address = row[1]
        flag = row[2]

        if(client_domain == hostname):
            return  ip_address       

    return False


def server():
    file_path = "PROJI-DNSRS.txt"

    listen_port = int(sys.argv[1])    

    dns_table = convertFileToArray(file_path)

    # create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except s.error as err:
        print('{} \n'.format("socket open error ",err))

    # bind the socket to an ip address and port number, using tuples: s.bind(<ip_address>, <port_number>)      
    s.bind((socket.gethostname(), listen_port))    
    
    host=socket.gethostname()
    print("[S]: Server host name is: " + host)
    
    localhost_ip=(socket.gethostbyname(host))
    print("[S]: Server IP address is " + localhost_ip)
    
    s.listen(1)

    # Server will listen forever
    while True:
        print("[S]: Server is listening...")

        # If a connection is heard, the clientSocket object and ip_address from the connection are unpacked into 
        # the 'clientsocket' and 'address' variables
        clientsocket, address = s.accept() 
        print "[S]: Got a connection request from a client at", address

        # recieving domain given by client
        client_domain = clientsocket.recv(100).decode('utf-8')
        print "\n[S]: Domain recieved from client: ",
        print client_domain

        # search for domain in dns_table
        dns_ipaddress = getDomainFromTable(dns_table, client_domain)

        if(dns_ipaddress == False):            
            serverMsg =  client_domain + ' - NS'                        
            print "[S]: Could not find domain. Sending '" + serverMsg + "' back to client\n"
            clientsocket.send(serverMsg.encode('utf-8'))
        else:
            serverMsg = client_domain + " " + dns_ipaddress + " A"
            print "[S]: Found domain.\n> Sending '" + serverMsg + "' back to client\n"
            clientsocket.send(serverMsg.encode('utf-8'))

        clientsocket.close()       

    s.close()
    exit()

server()

# Clearing a portnumber in use:
# fuser 50007/tcp -k