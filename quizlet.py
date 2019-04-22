import requests
from bs4 import BeautifulSoup

def get_set(url: str):
    """
    Usage: get_set( [link to quizlet study set] )
    Return Type: Dictionary

    Takes a url to a quizlet study set and returns a dictionary with terms as keys and definitions as values
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    output = {}

    sets = soup.find_all('span', class_='TermText notranslate lang-en')
    i = 0
    for card in sets:
        term = str(card)[43::][:-7]
        if i % 2 == 0:
            output[term] = str(sets[i + 1])[43::][:-7]
            i += 1
        else:
            i += 1
            continue
    
    return output