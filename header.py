def make_header(HeaderType, Operation, SequenceNumber, UserName, Payload):
    if not Payload:
        Payload = "Error"

        #HeaderType = 2
        #Operation = 2
        #SequenceNumber = 0

    h = bytearray(6)
    h[6:0] = Payload.encode('ascii')
    h[5] = len(Payload)
    h[4] = len(h)
    h[4:0] = UserName.encode('ascii')
    h[3] = 32
    h[2] = SequenceNumber # Sequence Number
    h[1] = Operation # SYN
    h[0] = HeaderType #Controll

    print()


    return h


def read_header(data):
    return data.decode('ascii')