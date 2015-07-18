import logging
import requests
import uuid

from django.utils import timezone
from django.conf import settings

from bloodhound.core.models import Product, Image
from bloodhound.sniffer.models import CrawlFrontier


class Bloodhound(object):
    
    def __init__(self):
        self.headers = { 'user-agent': 'bloodhound/1.0' }
        self.url = 'http://www.verkkokauppa.com/fi/'
        self.uuid = uuid.uuid4()

    def feed(self, url):
        frontier = None
        if url:
            frontier = CrawlFrontier(sniff_session=self.uuid, url=url)
            frontier.save()
        return frontier

    def crawl(self, frontier):
        r = requests.get(frontier.url, headers=self.headers)
        frontier.is_visited = True
        frontier.visited_at = timezone.now()
        frontier.status_code = r.status_code
        frontier.save()

        html = r.text
        tags = html.split('>')

        for tag in tags:
            try:
                if ' href="http://www.verkkokauppa.com/fi/' in tag:
                    splited_tag = tag.split(' href="')
                    link = splited_tag[1].partition('"')[0]
                    CrawlFrontier.objects.get_or_create(sniff_session=self.uuid, url=link)
                if ' href="http://www.verkkokauppa.com/fi/product/' in tag:
                    splited_tag = tag.split(' href="http://www.verkkokauppa.com/fi/product/')
                    product_code = splited_tag[1].partition("/")[0].partition("?")[0].partition("#")[0]
                    product, created = Product.objects.get_or_create(code=product_code)
                    if created:
                        self.howl(product_code)
            except:
                pass

    def sniff(self):
        while True:
            try:
                frontier = CrawlFrontier.objects.filter(sniff_session=self.uuid, is_visited=False).order_by('created_at')[0]
                self.crawl(frontier)
            except:
                break

    def howl(self, product):
        r = requests.get(product.get_url(), headers=self.headers)
        if r.status_code == 200:
            try:
                html = r.text
                product.name = html.split('class="product-name"')[1].split('>')[1].partition('<')[0]
                price = float(html.split('<meta itemprop="price" content="')[1].split('"')[0].partition(' ')[0].replace(',', '.'))
                if price:
                    product.update_price(price)
                    product.status = Product.OK
                else:
                    logging.error(u'Could not parse price for product {0} at {1}'.format(product.code, product.get_url()))

                try:
                    product.manufacturer = html.split('itemtype="http://schema.org/Organization"')[1].split('<td itemprop="name"><strong>')[1].partition('</strong>')[0]
                except:
                    logging.error(u'Could not parse manufacturer for product {0} at {1}'.format(product.code, product.get_url()))

                try:
                    product.manufacturer_code = html.split('itemtype="http://schema.org/Organization"')[1].split('<td itemprop="model"><strong>')[1].partition('</strong>')[0]
                except:
                    logging.error(u'Could not parse manufacturer code for product {0} at {1}'.format(product.code, product.get_url()))

                try:
                    image_tags = html.split('<meta property="og:image" content="')
                    for tag in image_tags:
                        image_url = tag.split('"')[0]
                        if 'http://cdn' in image_url:
                            Image.objects.get_or_create(product=product, url=image_url)
                except Exception, e:
                    logging.error(u'Could not parse images for product {0} at {1}'.format(product.code, product.get_url()))

                product.url = r.url
            except Exception, e:
                product.status = Product.ERROR
                logging.error(u'Could not parse product {0} at {1}. Exception {2}'.format(product.code, product.get_url(), e.message))
        elif r.status_code == 404:
            product.status = Product.NOT_FOUND
        else:
            product.status = Product.ERROR
            logging.error(u'URL {0} returned status code {1}'.format(r.url, r.status_code))
        product.save()
        return product
