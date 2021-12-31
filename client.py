import socket
import sys
import string
import header

def send(host, port) -> string:
    reply = None
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        if reply is None:
                while True:
                    user_name = input("Your username: ")
                    if len(user_name) > 32:
                        print("Username too long!")
                    if user_name:
                        break
                user_message = input("Enter message you want to send: ")
                print("Message sent, waiting for reply...")
                print("Waiting for connection on port:", port)
                HeaderType = 2
                Operation = 2
                SequenceNumber = 0
                data_send = header.make_header(HeaderType, Operation, SequenceNumber, user_name, user_message)
                s.sendto(data_send, (host, port))
        while True:
            s.settimeout(10.0)
            reply = s.recv(1024)
            s.settimeout(None)
            if reply[1] == 4:
                print("["+read_name(reply)+"]", reply[36:].decode('ascii'))
                user_message = input("Your message: ")
                if user_message == "quit":
                    HeaderType = 2
                    Operation = 8
                    SequenceNumber = 0
                    reply = header.make_header(HeaderType, Operation, SequenceNumber, user_name, user_message)
                    s.sendto(reply, (host, port))
                    break
                HeaderType = 1
                Operation = 4
                SequenceNumber = 0
                reply = header.make_header(HeaderType, Operation, SequenceNumber, user_name, user_message)
                s.sendto(reply, (host, port))
            if reply[1] == 8:
                print("["+read_name(reply)+"]", reply[36:].decode('ascii'))
                break

            if reply[1] == 6:
                print("Conncected by:", host, port)
                print("[" + read_name(reply) + "]", reply[36:].decode('ascii'))
                user_message = input("Your message: ")
                HeaderType = 2
                Operation = 4
                SequenceNumber = 0
                reply = header.make_header(HeaderType, Operation, SequenceNumber, user_name, user_message)
                s.sendto(reply, (host, port))

def read_name(package):
    name = package[5:35].decode(('ascii'))
    i = 0
    for char in name:
        if char == "0":
            i += 1
        else:
            break
    return name[i:]


data = send(sys.argv[1], int(sys.argv[2]))