import urllib
import re
import itertools

import BeautifulSoup

def extract_text(t):
    if not t:
        return ""
    if isinstance(t, (unicode, str)):
        return t
    return "".join(extract_text(c) for c in t)

def get(N, *PropertyCodeValues):
    res = []
    page = 1
    while True:
        print "Page", page
        data = {
            'Submit': 'Property',
            'N': str(N),
            'bop': 'And',
            'Pagesize': '100',
            'Page': str(page),
        }
        data = data.items()
        for PropertyCodeValue in PropertyCodeValues:
            data.append(('PropertyCodeValue', PropertyCodeValue))
        url = 'http://www.newegg.com/Product/ProductList.aspx?'+urllib.urlencode(data)
        print url
        text = urllib.urlopen(url).read()
        dom = BeautifulSoup.BeautifulSoup(text)
        pager = dom.find('input', {'name':'Page'})
        if not pager:
            print "lost pager"
            break
        pager = int(pager['value'])
        if pager != page:
            print "lost pager2"
            break
        for item in dom.findAll('div', {'class':'itemCell'}):
            dom_desc = item.find('span', {'class':'itemDescription'})
            title = dom_desc.contents[0]
            title += " " + extract_text(item.find('ul', {'class':'itemFeatures'}))
            link = dom_desc.parent['href']
            try:
                out = re.compile("([0-9.]+)([MGT])B").findall(title.upper())[0]
            except IndexError:
                print "invalid size", repr(title)
                continue
            size = float(out[0])
            if out[1] == 'M':
                size /= 1000.
            elif out[1] == 'T':
                size *= 1000.
            try:
                price = float(extract_text(item.find('li', {'class':'priceFinal'})).split('$')[1].replace(',',''))
            except:
                try:
                    price = float(extract_text(item.find('li', {'class':'priceList'})).split('$')[1].replace(',',''))
                except:
                    print "invalid price", repr(extract_text(item.find('li', {'class':'priceFinal'}))), repr(extract_text(item.find('li', {'class':'priceList'})))
                    continue
            yield size, price, title, link
        print "Page", page, "done"
        page += 1
