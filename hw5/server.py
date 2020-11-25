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
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # minimal level
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)  # higher level
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


class BertAPI():
    def __init__(self):
        self.bert = BertForMaskedLM.from_pretrained("./ruBert")
        self.tokenizer = BertTokenizer.from_pretrained("./ruBert")
        logger.info("successfully loaded BERT in ':memory:'")

    def predict(self, masked_string, topk):
        nlp = FillMaskPipeline(self.bert, self.tokenizer, topk)
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
    config = {'Port': int(config['DEFAULT']['Port']),
              'LogPath': config['DEFAULT']['LogPath'],
              'AsDaemon': config['DEFAULT']['AsDaemon'] == 'True',
              'ServerRecieveTimeOut': float(config['DEFAULT']
                                            ['ServerRecieveTimeOut']),
              'MaxConnections': int(config['DEFAULT']['MaxConnections']), }
    return config


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
    if not('string' in request.keys()):
        # log it and raise it
        raise KeyError("'string' key is required")
    result = nlp.predict(request['string'], request.get('topk', 5))
    result = {f"top {i+1}": el for i, el in enumerate(result)}
    result = format_result(result, request['format'])
    return result


def main(config, logger):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', config['Port']))  # Bind the socket to address
        # Enable a server to accept connections
        sock.listen(config['MaxConnections'])
        nlp = BertAPI()
        logger.info("successfully launched the server")
        while True:
            # Accept a connection. conn is a new socket
            conn, addr = sock.accept()
            st_req_time = time.time(), time.asctime()
            try:
                conn.settimeout(config['ServerRecieveTimeOut'])
                logger.info(f"connected: {addr}")
                request = conn.recv(4096)  # waits
                if not request:
                    conn.close()
                    continue
            except socket.timeout:
                conn.send(bytes("Server could not wait to "
                                "receive request", 'utf-8'))
                logger.error("Time Out: server waited too long for request")
                fin_req_time = time.time()
            else:
                conn.send(bytes("Processing ...", 'utf-8'))
                try:
                    result = parse_request(request, nlp)
                except Exception as ex:
                    conn.send(bytes("Something Wrong, check your "
                                    "request again\n", 'utf-8'))
                    logger.error("exception raised while parsing "
                                 f"and processing: {ex}")
                    # logit
                else:
                    result
                    conn.send(bytes(f'{result}', 'utf-8'))
                fin_req_time = time.time(), time.asctime()
                logger.info("CONNECTION INFO:"
                            f"started: {st_req_time[1]}, "
                            f"finished: {fin_req_time[1]}, duration (sec): "
                            f"{fin_req_time[0]- st_req_time[0]:.5f}")
            finally:
                conn.close()


if __name__ == '__main__':
    """
    https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
    """
    args = parse_args()
    config = parse_config(args)
    logger = get_logger(__name__, config['LogPath'])
    if config['AsDaemon']:
        context = daemon.DaemonContext(umask=0o002,
                                       working_directory='/home/dmitry/МАГА/'
                                       'python-backend/hw5',
                                       uid=1000, gid=1000)
        context.files_preserve = [logger.handlers[0].stream.fileno(),
                                  open('./ruBert/config.json'),
                                  open('./ruBert/pytorch_model.bin'),
                                  open('./ruBert/vocab.txt')]
        try:
            with context:
                main(config, logger)
        except Exception as ex:
            logger.error(f'exception raised while launching daemon: {ex}')
    else:
        main(config, logger)
