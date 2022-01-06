import socket
import sys
import header


def wait_and_receive(host, port):
    received_operation = 2
    received_sequence_con = 0
    received_sequence_message = 0
    client = 0
    connection = 1
    while True:
        user_name = input("Your username: ")
        if len(user_name) > 32:
            print("Username too long!")
        if user_name:
            break
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print('Waiting for connections...')
        s.bind((host, port))
        while True:
            if connection == 0:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print('Waiting for connections...')
                s.bind((host, port))
            if received_operation == 4:
                while True:
                    s.settimeout(10.0)
                    try:
                        package, host_from = s.recvfrom(1024)
                        break
                    except:
                        s.sendto(chat_message, host_from)
                    s.settimeout(None)
                if package[1] == 2 and client != 0:     #
                    chat_message = header.make_chat_message(1, 8, 1, user_name, "User already in another chat")
                    s.sendto(chat_message, host_from)
                    continue
            if received_operation != 4:
                package, host_from = s.recvfrom(1024)
                if package[1] == 2 and client != 0:
                    chat_message = header.make_chat_message(1, 8, 1, user_name, "User already in another chat")
                    s.sendto(chat_message, host_from)
                    continue
                if package[1] == 2 and client == 0:     #
                    client = 1
                print('Connected by', host_from)
            if not package:
                break
            if package[0] == 2 and package[1] == received_operation and package[2] == received_sequence_con:
                if received_operation == 2:
                    print("You got invited from", header.read_name(package), "accept? [Y/n]")
                    user_message = input()
                    if user_message == "N" or user_message == "n":
                        control_package = header.make_control_message(2, 8, 1, user_name)
                        s.sendto(control_package, host_from)
                        continue
                    if user_message == "Y" or user_message == "y":
                        pass
                    control_package = header.make_control_message(2, 6, 1, user_name)
                if received_operation == 4:
                    control_package = header.make_control_message(2, 4, 1, user_name)
                s.sendto(control_package, host_from)
                if received_operation == 4:
                    while True:
                        s.settimeout(10.0)
                        try:
                            package, host_from = s.recvfrom(1024)
                            break
                        except:
                            s.sendto(control_package, host_from)
                        s.settimeout(None)
                    if package[1] == 2 and client != 0:             #
                        chat_message = header.make_chat_message(1, 8, 1, user_name, "User already in another chat")
                        s.sendto(chat_message, host_from)
                        continue
                if received_operation != 4:
                    package, host_from = s.recvfrom(1024)           #
                    if package[1] == 2 and client != 0:
                        chat_message = header.make_chat_message(1, 8, 1, user_name, "User already in another chat")
                        s.sendto(chat_message, host_from)
                        continue
                received_operation = 4
                if package[0] == 1 and package[1] == 1 and package[2] == received_sequence_message:
                    print("[" + header.read_name(package) + "]", package[36:].decode('ascii'))
                    if package[36:].decode('ascii') == "quit":
                        received_operation = 2
                        received_sequence_con = 0
                        received_sequence_message = 0
                        client = 0
                        connection = 0
                        s.close()
                        continue
                    user_message = input("Enter Message to send:")
                    if user_message == "quit":
                        control_package = header.make_control_message(2, 8, 1, user_name)
                        s.sendto(control_package, host_from)
                        package, host_from = s.recvfrom(1024)
                        if package[1] == 4:
                            received_operation = 2
                            received_sequence_con = 0
                            received_sequence_message = 0
                            client = 0
                            connection = 0
                            s.close()
                            continue
                    chat_message = header.make_chat_message(1, 1, 1, user_name, user_message)
                    s.sendto(chat_message, host_from)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(1)

wait_and_receive(sys.argv[1], int(sys.argv[2]))
