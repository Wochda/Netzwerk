def make_header(HeaderType, Operation, SequenceNumber, UserName, Payload):
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
    package.append(len(message))
    package.extend(message)

    return package


def read_header():
    HeaderType = 2
    Operation = 2
    SequenceNumber = 0
    UserName = "jamann"
    Payload = "wos geht?"
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
    print(package)
    print(package[35])
    #package[1] = 6
    #print(package[1])
    #print(package)
    #print(package[36:])
    #package[36:] = bytearray("hoffentlich".encode('ascii'))
    #print(package[36:])
    #p = package[5:35].decode(('ascii'))

read_header()