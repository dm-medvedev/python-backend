#!/usr/bin/python3
import argparse
import socket
import time

from pprint import pprint
import json
from xml.dom.minidom import parseString


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help='request to server')
    args = parser.parse_args()
    return args


def from_format(result, args):
    format_ = [el for el in args.request.split('&') 
               if el.startswith('format')][0].split('=')[1]
    if format_ == 'json':
        pprint(json.loads(result))
    if format_ == 'xml':
        dom = parseString(result)
        print(dom.toprettyxml())
    return 


def main(args):
    sock = socket.socket()
    sock.connect(('127.0.0.1', 10033))
    print('connected')
    time.sleep(2)
    sock.sendall(args.request.encode('utf-8'))
    while True:
        data = sock.recv(4096)  # waits
        if not data:
            break
        data = data.decode('utf-8')
        if data.startswith('Processing'):
            print(data)
        else:
            from_format(data, args)
    sock.close()


if __name__ == '__main__':
    args = parse_args()
    main(args)
