#!usr/bin/env python
#encoding:utf-8
import re
import argparse


def judge_legal_ip(one_str):
    if one_str=="localhost":
        return True
    compile_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(one_str):
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="socket address")
    parser.add_argument('--host', default="localhost")
    parser.add_argument('--port', default="5678", type=int)
    args = parser.parse_args()
    print args.host

