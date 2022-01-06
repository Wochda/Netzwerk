def make_chat_message(HeaderType, Operation, SequenceNumber, UserName, Payload):
    if not Payload:
        Payload = "Error"

    username = UserName
    if len(username) < 32:
        username = "0" * (32 - len(username)) + username
        username = bytearray(username.encode('ascii'))
    message = bytearray(Payload.encode('ascii'))

    package = bytearray(0)
    package.append(HeaderType)
    package.append(Operation)
    package.append(SequenceNumber)
    package.extend(username)
    package.append(0)
    package.extend(message)
    package[4] = len(package)

    return package


def make_control_message(HeaderType, Operation, SequenceNumber, UserName):
    username = UserName
    if len(username) < 32:
        username = "0" * (32 - len(username)) + username
        username = bytearray(username.encode('ascii'))

    package = bytearray(0)
    package.append(HeaderType)
    package.append(Operation)
    package.append(SequenceNumber)
    package.extend(username)
    package.append(len(package))

    return package

def read_name(package):
    name = package[5:35].decode(('ascii'))
    i = 0
    for char in name:
        if char == "0":
            i += 1
        else:
            break
    return name[i:]