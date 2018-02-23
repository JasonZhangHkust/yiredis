def parse_message(data):
    try:
        command = data.strip().split(':')[0]
        if command == "GET":
            command, key = map(str.strip, data.strip().split(':'))
            return command, key
        else:
            command, key, value = map(str.strip, data.strip().split(':'))
    except:
        raise Exception("INPUT Error")
    return command, key, value

data="GET:"
c,k=parse_message(data)
print c