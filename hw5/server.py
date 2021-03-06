#!/usr/bin/python3
import argparse
import configparser
import json
import logging
import socket
import time

import daemon

import dicttoxml

from transformers import BertForMaskedLM, BertTokenizer, FillMaskPipeline


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


class BertAPI():
    def __init__(self):
        self.bert = BertForMaskedLM.from_pretrained("./ruBert")
        self.tokenizer = BertTokenizer.from_pretrained("./ruBert")
        logger.info("successfully loaded BERT in ':memory:'")

    def predict(self, masked_string, topk):
        nlp = FillMaskPipeline(self.bert, self.tokenizer, topk=topk)
        return nlp(masked_string)


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
    res['bert'] = {k: v for k, v in config['BERT'].items()}
    res['port'] = int(res['port'])
    res['as_daemon'] = res['as_daemon'] == 'True'
    res['server_recieve_time_out'] = float(res['server_recieve_time_out'])
    res['max_connections'] = int(res['max_connections'])
    return res


def format_result(nlp_result, format=None):
    if format == 'json':
        return bytes(json.dumps(nlp_result), 'utf-8')
    elif format == 'xml':
        return dicttoxml.dicttoxml(nlp_result)
    else:
        # залогировать
        raise ValueError("unknown format, use either 'json' or 'xml'")


def parse_request(request, nlp):
    request = request.decode('utf-8')
    request = {s.split('=')[0]: s.split('=')[1] for s in request.split("&")}
    if 'string' not in request:
        # log it and raise it
        raise KeyError("'string' key is required")
    result = nlp.predict(request['string'], int(request.get('topk', 5)))
    result = {f"top {i+1}": el for i, el in enumerate(result)}
    result = format_result(result, request['format'])
    return result


def process_client(sock, config, logger, nlp):
    conn, addr = sock.accept()
    st_req_time = time.time(), time.asctime()
    try:
        conn.settimeout(config['server_recieve_time_out'])
        logger.info(f"connected: {addr}")
        request = conn.recv(4096)  # waits
        if not request:
            conn.close()
            return
    except socket.timeout:
        conn.send(bytes("Server could not wait to "
                        "receive request", 'utf-8'))
        logger.error("Time Out: server waited too long for request")
    else:
        conn.send(bytes("Processing ...", 'utf-8'))
        try:
            result = parse_request(request, nlp)
        except Exception as ex:
            conn.send(bytes("Something Wrong, check your "
                            "request again\n", 'utf-8'))
            logger.error("exception raised while parsing "
                         f"and processing: {ex}")
        else:
            conn.send(result)
    finally:
        conn.close()
        fin_req_time = time.time()
        fin_req_time = time.time(), time.asctime()
        logger.info("CONNECTION INFO:"
                    f"started: {st_req_time[1]}, "
                    f"finished: {fin_req_time[1]}, duration (sec): "
                    f"{fin_req_time[0]- st_req_time[0]:.5f}")


def main(config, logger):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', config['port']))  # Bind the socket to address
        # Enable a server to accept connections
        sock.listen(config['max_connections'])
        nlp = BertAPI()
        logger.info("successfully launched the server")
        while True:
            # Accept a connection. conn is a new socket
            process_client(sock, config, logger, nlp)


if __name__ == '__main__':
    """
    https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
    """
    args = parse_args()
    config = parse_config(args)
    logger = get_logger(__name__, config['log_path'])
    if config['as_daemon']:
        context = daemon.DaemonContext(umask=0o002,
                                       working_directory='/home/dmitry/МАГА/'
                                       'python-backend/hw5',
                                       uid=1000, gid=1000)
        context.files_preserve = [logger.handlers[0].stream.fileno()] +\
                                 [open(fnm) for fnm in config['bert'].values()]
        try:
            with context:
                main(config, logger)
        except Exception as ex:
            logger.error(f'exception raised while launching daemon: {ex}')
    else:
        main(config, logger)
