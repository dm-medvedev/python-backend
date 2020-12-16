#!/usr/bin/python3
import argparse
import json
import socket
import threading
from pprint import pprint

from utils import fin_token, port, receive_msg

client_rcv_timeout = 5


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', type=str, help='path to files with urls')
    parser.add_argument('m', type=int, help='number of threads')
    args = parser.parse_args()
    return args


def make_request(url):
    try:
        sock = socket.socket()
        sock.connect(('127.0.0.1', port))
        sock.sendall((url+fin_token).encode('utf-8'))
        data = receive_msg(sock, client_rcv_timeout)
        pprint(json.loads(data))
    except Exception as ex:
        print(f'Something wrong with calling {url}: {ex}')
    finally:
        sock.close()


def main(args):
    with open(args.urls) as f:
        urls = [url.strip() for url in f.readlines()]
    while len(urls) > 0:
        threads = [
            threading.Thread(target=make_request, args=(urls.pop(),))
            for _ in range(min(args.m, len(urls)))
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()


if __name__ == '__main__':
    args = parse_args()
    main(args)
