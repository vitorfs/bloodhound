import requests

class Bloodhound(object):
    
    def __init__(self):
        self.headers = { 'user-agent': 'bloodhound/1.0' }
        self.url = 'http://www.verkkokauppa.com/fi/'
        self.products = set()
    
    def sniff(self):
        print 'Sniffing...'
        r = requests.get('http://www.verkkokauppa.com/', headers=self.headers)
        html = r.text
        tags = html.split('>')

        links = set()
        products = set()

        link_url = u' href="{0}'.format(self.url)
        product_url = u' href="{0}product/'.format(self.url)

        for tag in tags:
            if link_url in tag:
                splited_tag = tag.split(' href="')
                link = splited_tag[1].partition('"')[0]
                links.add(link)
            if product_url in tag:
                splited_tag = tag.split(' href="http://www.verkkokauppa.com/fi/product/')
                product = splited_tag[1].partition("/")[0].partition("?")[0].partition("#")[0]
                products.add(product)

        for link in links:
            print link

        for product in products:
            print product
            self.howl(product)

    def howl(self, product_id):
        product_url = u'{0}product/{1}'.format(self.url, product_id)
        r = requests.get(product_url, headers=self.headers)
        html = r.text
        price = ''
        name = ''

        try:
            price = html.split('<meta itemprop="price" content="')[1].partition('"')[0]
        except:
            pass

        try:
            name = html.split('class="product-name"')[1].split(">")[1].partition('<')[0]
        except:
            try:
                name = html.split('<title>')[1].partition('|')[0]
            except:
                pass

        print u'{0} {1}'.format(name, price)
