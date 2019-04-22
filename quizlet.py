import requests
from bs4 import BeautifulSoup

class Quizlet():
    def __init__(self, *args):
        self.urls = list(args)
        self.term_dict = {}
        self.terms = []
        self.definitions = []
    def get_dict(self):
        for url in self.urls:
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')

            cards = soup.find_all('span', class_='TermText notranslate lang-en')
            i = 0
            for card in cards:
                term = str(card)[43::][:-7]
                if i % 2 == 0:
                    self.term_dict[term] = str(cards[i + 1])[43::][:-7]
                    i += 1
                else:
                    i += 1
                    continue