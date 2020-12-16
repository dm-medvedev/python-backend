import re
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from io import StringIO

prefix = '<td><i><a href="/wiki/'
url_prefix = 'https://ru.wikipedia.org/wiki/'
pc_games_url = 'https://en.wikipedia.org/wiki/'\
               'List_of_best-selling_PC_games'
game_ref = re.compile(f'{prefix}[\w ]+"')
fin_token = "<FIN>"
port = 10010


def get_pc_games_urls():
    data = urllib.request.urlopen(pc_games_url)
    games = []
    for line in data:
        games += game_ref.findall(line.decode("utf-8"))
    games = [url_prefix + game[len(prefix):-1] for game in games]
    return games


def receive_msg(conn, timeout):
    data = ''
    while True:
        answer = conn.recv(4096)
        data += answer.decode('utf-8')
        if answer.endswith(bytes(fin_token, 'utf-8')):
            break
        if not answer:
            raise ValueError('Wrong final tooken')
    return data[:-len(fin_token)]


class MLStripper(HTMLParser):
    """
    https://stackoverflow.com/questions/753052/\
    strip-html-from-strings-in-python
    """
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def get_top(url, top_k=5, max_sz=100_000):
    words = []
    data = urllib.request.urlopen(url)
    regex = re.compile('[A-Za-zА-Яа-яёЁ]+\-?[A-Za-zА-Яа-яёЁ]+')
    for line in data.readlines(max_sz):
        stripper = MLStripper()
        stripper.feed(line.decode("utf-8"))
        words += regex.findall(stripper.get_data().strip())
    counter = Counter(words)
    result = {i: word for i, (word, _) in
              enumerate(counter.most_common(top_k))}
    return result
