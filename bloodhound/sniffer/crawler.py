import requests
import uuid

from django.utils import timezone

from bloodhound.core.models import Product
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
    
    def sniff(self):
        frontier = CrawlFrontier.objects.filter(sniff_session=self.uuid, is_visited=False).order_by('created_at')

        if frontier.exists():
            crawl = frontier[0]
            r = requests.get(crawl.url, headers=self.headers)
            crawl.is_visited = True
            crawl.visited_at = timezone.now()
            crawl.status_code = r.status_code
            crawl.save()

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
                        Product.objects.get_or_create(code=product_code)
                except:
                    pass

            self.sniff()


    def howl(self, product_code):
        default_product_url = u'{0}product/{1}'.format(self.url, product_code)
        product, created = Product.objects.get_or_create(code=product_code, defaults={ 'url': default_product_url })
        if not product.url:
            product.url = default_product_url
        r = requests.get(product.url, headers=self.headers)

        if r.status_code == 200:
            try:
                html = r.text
                product.name = html.split('class="product-name"')[1].split(">")[1].partition('<')[0]
                price = float(html.split('<meta itemprop="price" content="')[1].split('"')[0].partition(' ')[0].replace(',', '.'))
                product.update_price(price)
                product.url = r.url
                product.status = Product.OK
            except Exception, e:
                print e.message
                product.status = Product.ERROR
        else:
            product.status = Product.ERROR

        product.save()
