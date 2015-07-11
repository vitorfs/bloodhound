import requests

class Bloodhound(object):

    headers = { 'user-agent': 'bloodhound/1.0' }
    
    def __init__(self):
        super(Bloodhound, self).__init__()
    
    def sniff(self):
        print 'Sniffing...'
        r = requests.get('http://www.verkkokauppa.com/', headers=self.headers)
        html = r.text
        tags = html.split('>')

        links = set()
        products = set()

        for tag in tags:
            if ' href="http://www.verkkokauppa.com/fi/' in tag:
                splited_tag = tag.split(' href="')
                link = splited_tag[1].partition('"')[0]
                links.add(link)
            if ' href="http://www.verkkokauppa.com/fi/product/' in tag:
                splited_tag = tag.split(' href="http://www.verkkokauppa.com/fi/product/')
                product = splited_tag[1].partition("/")[0].partition("?")[0].partition("#")[0]
                products.add(product)

        for link in links:
            print link

        for product in products:
            print product
