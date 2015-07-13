from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhound.settings')

import django
django.setup()


import threading
from bloodhound.sniffer.crawler import Bloodhound


class Sniff(threading.Thread):

    def __init__(self):
        super(Sniff, self).__init__()
        self.crawler = Bloodhound()
        self.crawler.feed('http://www.verkkokauppa.com/')

    def run(self):
        self.crawler.sniff()


def main():
    crawling = Sniff()
    crawling.start()

if __name__ == '__main__':
    main()
