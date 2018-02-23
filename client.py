#!/usr/bin/env python
import argparse
import socket
import cmd
import sys
authed = "-1"


def parse_message(data):
    command = None
    key = None
    value = None
    try:
        command = data.strip().split(' ')[0]
        if command.upper() == "GET":
            command, key = map(str.strip, data.strip().split(' '))
            return command.upper(), key, value
        elif command.upper() in ["AUTH","URL","SET"]:
            command, key, value = map(str.strip, data.strip().split(' '))
    except Exception as e:
        print e
    return command.upper(), key, value


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="socket address")
    parser.add_argument('--host', default="localhost")
    parser.add_argument('--port', default="5678", type=int)
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))
    while True:
        try:
            raw_cmd = raw_input('yiRedis>> ')
            if raw_cmd == "exit":
                sock.send(raw_cmd)
                break
            command, key, value = parse_message(raw_cmd)
            if command == "URL" and authed != "0":
                print "Please AUTH before URL"
                continue
            if not value:
                sock.send(command+":"+key)
            else:
                sock.send(command+":"+key+":"+value)
            szBuf = sock.recv(1024)
            if command == "AUTH":
                authed=szBuf
            print("" + szBuf)
        except socket.error:
            exit(1)
        except TypeError:
            print "Error Command Please Check"
