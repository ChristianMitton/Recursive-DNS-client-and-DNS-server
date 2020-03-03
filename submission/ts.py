import socket
import sys

#* .AF_INET corresponds to IPV4
#* SOCK_STREAM corresponds to TCP

def convertFileToArray(file_path):
    f = open(file_path, "r")

    result = []

    contents = f.readlines()

    for line in contents:        
        line = line.rstrip('\n')
        line = line.rstrip('\r')

        # split current line in file on space character
        splitString = line.split()        

        result.append(splitString)

    f.close() 
    return result    

def getDomainFromTable(dns_table, client_domain):
    for row in dns_table:        
        hostname = row[0]
        ip_address = row[1]
        flag = row[2]

        if(client_domain == hostname):
            entry = ' '.join(row)
            return entry

    return False

def server():
    file_path = "PROJI-DNSTS.txt"

    listen_port = int(sys.argv[1])    

    dns_table = convertFileToArray(file_path)

    # create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS Server socket created")
    except s.error as err:
        print('{} \n'.format("socket open error ",err))

    # bind the socket to an ip address and port number, using tuples: s.bind(<ip_address>, <port_number>)    
    s.bind((socket.gethostname(), listen_port))    
    
    host=socket.gethostname()
    print("[S]: TS Server host name is: " + host)
    
    localhost_ip=(socket.gethostbyname(host))
    print("[S]: TS Server IP address is " + localhost_ip)

    #* print('Server is Listening...')
    s.listen(1)

    # Server will listen forever
    while True:
        print("[S]: TS Server is listening...")

        # If a connection is heard, the clientSocket object and ip_address from the connection are unpacked into 
        # the 'clientsocket' and 'address' variables
        clientsocket, address = s.accept() 
        print "[S]: Got a connection request from a client at", address        

        # recieving word given by client
        client_domain = clientsocket.recv(100).decode('utf-8')
        print "\n[S]: Domain recieved from client: ",
        print client_domain

        # search for domain in dns_table
        dns_ipaddress = getDomainFromTable(dns_table, client_domain)

        if(dns_ipaddress == False):            
            serverMsg = client_domain + ' - Error:HOST NOT FOUND'                        
            print "[S]: Could not find domain. Sending '" + serverMsg + "' back to client\n"
            clientsocket.send(serverMsg.encode('utf-8'))
        else:
            serverMsg = dns_ipaddress
            print "[S]: Found domain.\n> Sending '" + serverMsg + "' back to client\n"
            clientsocket.send(serverMsg.encode('utf-8'))        

        clientsocket.close()       

    s.close()
    exit()

server()