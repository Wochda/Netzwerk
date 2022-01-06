import socket
import sys
import header


def send(host, port):
    operation = 2
    sequence_con = 0
    sequence_message = 0
    print("SIMP Client 1.0.0")
    while True:
        user_name = input("Your username: ")
        if len(user_name) > 32:
            print("Username too long!")
        if user_name:
            break
    user_message = input("Enter Message to send:")
    if user_message == "quit":
        exit(1)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((host, port))
        control_package = header.make_control_message(2, operation, sequence_con, user_name)
        s.sendto(control_package, (host, port))
        operation = 6
        sequence_con = 1
        chat_message = header.make_chat_message(1, 1, sequence_message, user_name, user_message)
        s.sendto(chat_message, (host, port))
        sequence_message = 1
        while True:
            if operation == 4:
                while True:
                    s.settimeout(10.0)
                    try:
                        reply = s.recv(1024)
                        break
                    except:
                        s.sendto(chat_message, (host, port))
                    s.settimeout(None)
            if operation != 4:
                reply = s.recv(1024)
            if reply[0] == 2 and reply[1] == operation and reply[2] == sequence_con:
                control_package = header.make_control_message(2, 4, 0, user_name)
                s.sendto(control_package, (host, port))
                if operation == 4:
                    while True:
                        s.settimeout(10.0)
                        try:
                            reply = s.recv(1024)
                            break
                        except:
                            s.sendto(control_package, (host, port))
                        s.settimeout(None)
                if operation != 4:
                    reply = s.recv(1024)
                operation = 4
                if reply[0] == 1 and reply[1] == 1 and reply[2] == sequence_message:
                    print("[" + header.read_name(reply) + "]", reply[36:].decode('ascii'))
                    user_message = input("Enter Message to send:")
                    chat_message = header.make_chat_message(1, 1, 0, user_name, user_message)
                    s.sendto(chat_message, (host, port))
                    if user_message == "quit":
                        control_package = header.make_control_message(2, 8, 0, user_name)
                        s.sendto(control_package, (host, port))
                        reply = s.recv(1024)
                        if reply[1] == 4 and reply[0] == 2:
                            break
            if reply[0] == 2 and reply[1] == 8 and reply[2] == sequence_con:
                print(header.read_name(reply), "disconnected")
                break
            if reply[0] == 1 and reply[1] == 8 and reply[2] == sequence_con:
                print("[" + header.read_name(reply) + "]", reply[36:].decode('ascii'))
                break

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(1)

send(sys.argv[1], int(sys.argv[2]))
