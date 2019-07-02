import os
import sys
import bs4
from bs4 import BeautifulSoup
import re


class EmailParser():

    def __init__(self, pathToHtml = None, html = None):
        self.price = ''
        self.elementParsed = ''
        self.textSearch = [
            'Order Total',
            'Order total',
            'Total including tax',
            'Total',
            'Amount',
            'amount',
            'Balance',
            'Current Charges',
            'ORDER TOTAL'
        ]
        self.op = '|'
        self.currencies = [
            '$',
            'Rs'
        ]
        if os.path.isfile(pathToHtml):
            self.html = open(pathToHtml).read()
        elif html is not None:
            print 'came here'
            self.html = html
        else:
            print("please give correct path to file")
            sys.exit(1)

    def encodeString(self, string):
        return string.encode('utf-8').replace("\xc2\xa0", " ").strip()

    def findNextNotNone(self, element):
        try:
            currencyMatch = False
            if isinstance(element, bs4.element.NavigableString):
                for currency in self.currencies:
                    if currency in self.encodeString(element):
                        currencyMatch = True
                        self.elementparsed = self.encodeString(element)
            if currencyMatch is False:
                self.elementparsed = self.encodeString(element.next_element.text)
            if self.elementparsed != '':
                self.price = self.elementparsed
            else:
                self.findNextNotNone(element.next_element)
        except:
            self.findNextNotNone(element.next_element)

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        for elem in soup.body.findAll(text=re.compile('.*('+self.op.join(self.textSearch)+')')):
            self.findNextNotNone(elem)
            if self.price != '':
                print elem.encode('utf-8').strip(), self.price.strip()



def main():
        userInput = raw_input("Enter the html path? \n")
        emailParser = EmailParser(pathToHtml = userInput)
        emailParser.parse()

if __name__ == "__main__":
        main()
