import socket
import sys


# * .AF_INET corresponds to IPV4
# * SOCK_STREAM corresponds to TCP

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


def client():
    f = open("RESOLVED.TXT", 'w')
    file_path = sys.argv[1] + ""

    rs_listen_port = int(sys.argv[2])

    ts_listen_port = int(sys.argv[3])

    host_names = convertFileToArray(file_path)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("[C]: Client socket created")

    except s.error as err:
        print('{} \n'.format("socket open error ", err))

    connection = (socket.gethostbyname(socket.gethostname()), rs_listen_port)
    s.connect(connection)

    # Connect to TS server
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("[C]: Client socket created")
    except ts.error as err:
        print('{} \n'.format("socket open error ", err))

    connection = (socket.gethostbyname(socket.gethostname()), ts_listen_port)
    ts.connect(connection)

    for user_domain in host_names:
        user_domain = user_domain[0]

        # sending user word to server
        # s.send(word.encode('utf-8'))
        s.send(user_domain.encode('utf-8'))

        # recieving converted word from server
        rs_server_response = s.recv(100)

        decodedWord = rs_server_response.decode('utf-8')

        splitString = decodedWord.split()

        if splitString[2] == "NS":
            ts.send(user_domain.encode('utf-8'))

            ts_server_response = ts.recv(100)

            decodedWord = ts_server_response.decode('utf-8')
        f.write(decodedWord + '\n')

    s.close()
    ts.close()
    f.close()
    exit()


client()

# print("Arguments:\n> " + sys.argv[0] + "\n> " + sys.argv[1])
