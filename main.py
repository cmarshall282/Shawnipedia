from quizlet import Quizlet
from docswriter import DocsWriter

def main():
    quizlet = Quizlet('https://quizlet.com/295732026/ap-world-history-2018-flash-cards/')
    docswriter = DocsWriter('1dRZAWl_b9RqvrvIRM5q5XxtE5NcmeopazRk23qJshzk')

    terms = docswriter.get_terms()

    for term in terms:
        definition = quizlet.define(term)
        docswriter.replace_text('*' + term, definition)

    docswriter.update_file()

if __name__ == '__main__':
    main()