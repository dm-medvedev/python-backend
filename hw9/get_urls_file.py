#!/usr/bin/python3
import argparse

from utils import get_pc_games_urls


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='file name to save urls')
    args = parser.parse_args()
    return args


def main(args):
    urls = get_pc_games_urls()
    with open(args.filename, 'w') as f:
        f.writelines(url+'\n' for url in urls)


if __name__ == '__main__':
    """
    https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
    """
    args = parse_args()
    main(args)