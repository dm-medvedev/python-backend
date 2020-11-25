import argparse
import socket


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help='request to server')
    args = parser.parse_args()
    return args


def main(args):
    sock = socket.socket()
    sock.connect(('127.0.0.1', 10023))
    print('connected')
    # time.sleep(100000000)
    sock.sendall(args.request.encode('utf-8'))
    while True:
        data = sock.recv(4096)  # waits
        if not data:
            break
        print(data.decode('utf-8'))
    sock.close()
    print(data.decode('utf-8'))


if __name__ == '__main__':
    args = parse_args()
    main(args)
