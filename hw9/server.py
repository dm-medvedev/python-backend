#!/usr/bin/python3
import argparse
import configparser
import json
import logging
import multiprocessing
import signal
import socket
import sys
import time
from collections import deque

from utils import fin_token, get_top, port, receive_msg

WAIT_PROCESS = 5


def get_logger(name, log_path):
    """
    name - module name

    https://docs.python.org/3/howto/logging.html
    https://docs.python.org/3/howto/logging-cookbook.html

    Должно быть указано время начала обработки запроса,
    время окончания запроса, затраченное на обработку запроса время,
    размер ответа и т.д.
    """
    is_path_empty = log_path == ''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # minimal level
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    if not is_path_empty:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if is_path_empty
                             else logging.ERROR)  # higher level
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='config INI file')
    args = parser.parse_args()
    return args


def parse_config(args):
    config = configparser.ConfigParser()
    with open(args.config) as f:
        config.read_file(f)
    res = {k: v for k, v in config['GENERAL'].items()}
    res['top_k'] = int(res['top_k'])
    res['n_workers'] = int(res['n_workers'])
    res['server_recieve_time_out'] = float(res['server_recieve_time_out'])
    return res


class Server():
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def _format_result(self, result):
        return json.dumps(result)

    def _parse_request(self, request, top_k):
        result = {}
        result['url'] = request
        try:
            result['top'] = get_top(request, top_k)
        except Exception as ex:
            self.logger.error("exception raised while parsing "
                              f"and processing: {ex}")
            result['error'] = "Something Wrong, check your request again"
        return self._format_result(result)

    def _signal_handler(self, signal_num, frame):
        print("Server shut down: successfully "
              f"processed {self.counter.value} urls")
        sys.exit(0)

    def _send_msg(self, conn, msg):
        conn.sendall(bytes(f"{msg}{fin_token}", 'utf-8'))

    def _process_client(self, conn):
        st_req_time = time.time(), time.asctime()
        request = None
        try:
            conn.settimeout(self.config['server_recieve_time_out'])
            request = receive_msg(conn, self.config['server_recieve_time_out'])
        except socket.timeout:
            msg = self._format_result({'error': "Server could not wait"
                                                " to receive request"})
            self._send_msg(conn, msg)
            self.logger.error("Time Out: server waited too long for request")
        else:
            result = self._parse_request(request, self.config['top_k'])
            self.logger.info(f"started processing: {request}")
            self._send_msg(conn, result)
            with self.counter.get_lock():
                self.counter.value += 1
        finally:
            fin_req_time = time.time()
            fin_req_time = time.time(), time.asctime()
            self.logger.info("CONNECTION INFO:"
                             f"started: {st_req_time[1]}, "
                             f"finished: {fin_req_time[1]}, duration (sec): "
                             f"{fin_req_time[0]- st_req_time[0]:.5f} "
                             f"url: {request}")
            conn.close()
            sys.exit(0)

    def clear_procs(self, procs):
        if len(procs) >= self.config['n_workers']:
            proc, conn = procs.popleft()
            proc.join(WAIT_PROCESS)
            # for proc, conn in procs:
            if proc.is_alive():
                proc.terminate()
            try:
                msg = self._format_result({'error': "too big site"})
                self._send_msg(conn, msg)
                conn.close()
            except Exception:
                pass
        return deque([])

    def start(self):
        procs = deque([])
        self.counter = multiprocessing.Value('i', 0, lock=True)
        signal.signal(signal.SIGUSR1, self._signal_handler)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('', port))  # Bind the socket to address
            # Enable a server to accept connections
            sock.listen(self.config['n_workers'])
            self.logger.info("successfully launched the server")
            while True:
                self.clear_procs(procs)
                self.logger.info(f'ACTIVE processes: {len(procs)}')
                conn, addr = sock.accept()
                self.logger.info(f"connected: {addr}")
                proc = multiprocessing.Process(target=self._process_client,
                                               args=(conn,))
                proc.daemon = True
                proc.start()
                procs.append((proc, conn))


def main(config, logger):
    server = Server(config, logger)
    server.start()


if __name__ == '__main__':
    """
    https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
    """
    args = parse_args()
    config = parse_config(args)
    logger = get_logger(__name__, config['log_path'])
    main(config, logger)
