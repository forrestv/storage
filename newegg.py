#!/usr/bin/python
import urllib
import BeautifulSoup
import re
import itertools

def get(N, *PropertyCodeValues):
    res = []
    for page in xrange(1, 100000):
        print page
        data = {
            'Submit': 'Property', # if PropertyCodeValue else 'ENE',
            'N': str(N),
            'bop': 'And',
            'Pagesize': '100',
            'Page': str(page),
        }
        data = data.items()
        for PropertyCodeValue in PropertyCodeValues:
            data.append(('PropertyCodeValue', PropertyCodeValue))
        url = 'http://www.newegg.com/Product/ProductList.aspx?'+urllib.urlencode(data)
        text = urllib.urlopen(url).read()
        open("c/"+url.replace('/',''),'w').write(text)
        dom = BeautifulSoup.BeautifulSoup(text)
        header = dom.find('dd', {'class':'addToCart'}).parent.parent.parent.parent
        if not header:
            print "lost header"
            break
        pager = dom.find('span', {'class':'newPaging'})
        if not pager:
            print "lost pager"
            break
        pager = int(pager.find('span', {'id':'active'}).contents[0])
        if pager != page:
            print "lost pager2"
            break
        items = header.contents
        for item in itertools.islice(items, 1, None, 6):
            title = item.h3.a.contents[0]
            if item.h3.contents[0] is not item.h3.a:
                title = item.h3.contents[0] + title
            link = item.h3.a['href']
            out = re.compile(" ([0-9.]*)([MGT])B ").findall(title)[0]
            size = float(out[0])
            if out[1] == 'M':
                size /= 1000.
            elif out[1] == 'T':
                size *= 1000.
            price = float(item.find(text=re.compile("Your Price:")).split('$')[1])
            yield size, price, title, link
