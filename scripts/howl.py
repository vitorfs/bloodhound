from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhound.settings')

import django
django.setup()


import threading
from bloodhound.core.models import Product
from bloodhound.sniffer.crawler import Bloodhound


class Howl(threading.Thread):

    def __init__(self):
        super(Howl, self).__init__()
        self.crawler = Bloodhound()

    def run(self):
        while True:
            products = Product.objects.all().order_by('visited_at')
            for product in products:
                self.crawler.howl(product)

def main():
    crawling = Howl()
    crawling.start()

if __name__ == '__main__':
    main()
