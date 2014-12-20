import urllib
import urllib2
import re
import itertools
import traceback
import string
import BeautifulSoup
import cookielib

def extract_text(t):
    if not t:
        return ""
    if t == '&ndash;': return ''
    if isinstance(t, (unicode, str)):
        return t
    return "".join(extract_text(c) for c in t)

def extract_price(data):
    res = sorted(float(x.replace(',', '')) for x in re.findall('\$([,0-9.]+)', data))
    if not res: raise ValueError('no price in %r' % (data,))
    return res[len(res)//2]
    

def get(N, *PropertyCodeValues):
    res = []
    page = 1
    while True:
        print "Page", page
        data = {
            'Submit': 'Property',
            'bop': 'And',
            'Pagesize': '100',
            'Page': str(page),
        }
        if isinstance(N, dict):
            data.update((k, str(v)) for k, v in N.iteritems())
        else:
            data['N'] = str(N)
        data = data.items()
        for PropertyCodeValue in PropertyCodeValues:
            data.append(('PropertyCodeValue', PropertyCodeValue))
        url = 'http://www.newegg.com/Product/ProductList.aspx?'+urllib.urlencode(data)
        print url
        
        req = urllib2.Request(url)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        text = opener.open(req).read()
        text = opener.open(req).read()
        
        dom = BeautifulSoup.BeautifulSoup(text)
        pager = dom.find('li', {'name':'currentPage'})
        if not pager:
            print "lost pager"
            break
        pager = int(extract_text(pager))
        if pager != page:
            print "lost pager2"
            break
        for item in dom.findAll('div', {'class':'itemCell'}):
            #print "-----------------------\n\n"
            dom_desc = item.find('span', {'class':'itemDescription'})
            title = dom_desc.contents[0]
            title += " " + extract_text(item.find('ul', {'class':'itemFeatures'}))
            link = dom_desc.parent['href']
            rating = item.findAll('a', {'class':'itemRating'})
            eggs = "0"
            for pk in rating:
                #print "pk: " + str(pk)
                pks = pk.findAll('span', limit=1)
                #print str(pk.findNextSibling(text))
                for pks_i in pks:
                    eggs = str(pks_i['class'])[6]
                    if len(eggs) == 0:
                        eggs = "0"
            votes = str(extract_text(rating))
            if len(votes) > 8:
                votes = votes[8:len(votes)-1]
            else:
                votes = "0"
            #print "title: " + title
            #print "link: " +link
            #print "eggs: " + eggs + " votes: " + votes

            try:
                out = re.compile("[^0-9A-Za-z.]([0-9.]+)( )?([MGT])B").findall(title.upper())[0]
            except IndexError:
                print "invalid size", repr(title)
                continue
            size = float(out[0])
            if out[2] == 'M':
                size /= 1000.
            elif out[2] == 'T':
                size *= 1000.
            try:
               price = extract_price(extract_text(item))
            except:
             traceback.print_exc()
             try:
                 price = float(extract_text(item.find('li', {'class':'price-current'})).split('$')[1].replace(',',''))
             except:
                traceback.print_exc()
                try:
                    price = float(extract_text(item.find('li', {'class':'priceBefore'})).split('$')[1].replace(',',''))
                except:
                    traceback.print_exc()
                    #print "invalid price", repr(extract_text(item.find('li', {'class':'priceFinal'}))), repr(extract_text(item.find('li', {'class':'priceList'})))
                    continue
            yield size, price, title, link, votes, eggs
        print "Page", page, "done"
        page += 1
