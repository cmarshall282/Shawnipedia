import requests
from bs4 import BeautifulSoup

class Quizlet():
    def __init__(self, *args):
        self.urls = list(args)
        self.cards = []
        self.term_dict = {}
        self.terms = []
        self.definitions = []
    def get_cards(self):
        """
        Usage: [Quizlet instance].get_cards()

        Initializes the list of cards to contain all terms AND definitions, used for
        the dictionary, the list of terms, and the list of definitions

        NOTE: All terms and definitions are LOWERCASE
        """
        for url in self.urls:
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            cards = soup.find_all('span', class_='TermText notranslate lang-en') # Find all classes containing either terms or definitions
            for card in cards:
                item = str(card)[43::][:-7] # Slicing to remove html text
                item = item.lower() # Making everything lowercase for consistency
                self.cards.append(item)
    def get_dict(self):
        """
        Usage: [Quizlet instance].get_dict()

        Initializes the dictionary in which the terms are stored as keys,
        and the definitions are stored as values in the dictionary
        """
        if self.cards == []: # Initialize cards if not done already
            self.get_cards()
        i = 0
        for card in self.cards:
            if i % 2 == 0:
                self.term_dict[card] = self.cards[i + 1]
                i += 1
            else:
                i += 1
                continue
    def get_terms(self):
        """
        Usage: [Quizlet instance].get_terms()

        Saves a list of terms collected from all given urls to study sets
        """
        if self.cards == []: # Initialize cards if not done already
            self.get_cards()
        i = 0
        for card in self.cards:
            if i % 2 == 0:
                self.terms.append(card) # Adding terms only (terms are at all even-numbered indexes)
                i += 1
            else:
                i += 1
                continue
    def get_definitions(self):
        """
        Usage: [Quizlet instance].get_definitions()

        Saves a list of definitions collected from all given urls to study sets
        """
        if self.cards == []:
            self.get_cards()
        i = 0
        for card in self.cards:
            if i % 2 == 1:
                self.definitions.append(card) # Adding definitions only (terms are at all odd-numbered indexes)
                i += 1
            else:
                i += 1
                continue