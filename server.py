import socket
import sys
import header


def wait_and_receive(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        while True:
            user_name = input("Your username: ")
            if len(user_name) > 32:
                print("Username too long!")
            if user_name:
                break
        print('Waiting for connection on port:', port)
        while True:
            s.settimeout(60.0)
            try:
                package, host_from = s.recvfrom(1024)
            except:
                print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
                break
            s.settimeout(None)
            if package[1] == 2:
                print("Connected by", host_from)
                print("["+read_name(package)+"]", package[36:].decode('ascii'))
                user_message = input("Your message: ")
                HeaderType = 2
                Operation = 6
                SequenceNumber = 1
                package = header.make_header(HeaderType, Operation, SequenceNumber, user_name, user_message)
                print("WWWW ", package)
                s.sendto(package, host_from)
            if package[1] == 4:
                print("["+read_name(package)+"]", package[36:].decode('ascii'))
                user_message = input("Your message: ")
                HeaderType = 1
                Operation = 4
                SequenceNumber = 1
                package = header.make_header(HeaderType, Operation, SequenceNumber, user_name, user_message)
                if user_message == "quit":
                    HeaderType = 2
                    Operation = 8
                    SequenceNumber = 1
                    package = header.make_header(HeaderType, Operation, SequenceNumber, user_name, user_message)
                    s.sendto(package, host_from)
                    break
                s.sendto(package, host_from)
            if package[1] == 8:
                print("["+read_name(package)+"]", package[36:].decode('ascii'))
                break
            if not package:
                break

def read_name(package):
    name = package[5:35].decode(('ascii'))
    i = 0
    for char in name:
        if char == "0":
            i += 1
        else:
            break
    return name[i:]


wait_and_receive(sys.argv[1], int(sys.argv[2]))