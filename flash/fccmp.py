#!/usr/bin/python

# Originally stcmp.py by Forrest Voight
# Minor modifications by Andrew Mashchak

import urllib
from BeautifulSoup import BeautifulSoup
import re
import Gnuplot, Gnuplot.funcutils

# Term, URL
# (I ought to add auto-handling of multipage searches)
searches = [ 
	("microSD",       'http://www.newegg.com/Product/ProductList.aspx?Submit=Property&Subcategory=68&N=2070070068&PropertyCodeValue=531%3A18914&PropertyCodeValue=531%3A31144&Pagesize=100'),
	("miniSD",        'http://www.newegg.com/Product/ProductList.aspx?Submit=Property&Subcategory=68&N=2070070068&PropertyCodeValue=531%3A14916&PropertyCodeValue=531%3A25687&Pagesize=100'),
	("SecureDigital", 'http://www.newegg.com/Product/ProductList.aspx?Submit=Property&Subcategory=68&N=2070070068&PropertyCodeValue=531%3A7930&PropertyCodeValue=531%3A25651&Pagesize=100'),
	("CompactFlash",  'http://www.newegg.com/Product/ProductList.aspx?Submit=Property&Subcategory=68&N=2070070068&PropertyCodeValue=531%3A7923&Pagesize=100'),
]


f = open("result/flash.txt","w")

g = Gnuplot.Gnuplot(debug=0)

g.xlabel('Size in GB')
g.ylabel('GB/$');
g("set logscale x 2")
g("set key left top")
g.set_string("output","result/flash.png")

g("set terminal png size 600,400 nocrop x000000 xFFFFFF xFFFFFF xFF0000 x00FF00 x0000FF")
g("set border 3")
g("set xtics nomirror")
g("set ytics nomirror")

plotdata = []	# collect plot data for plotting at end. - shouldn't be necessary, but couldn't get replot to work
count = 0

for entry in searches: 
 myitems = []
 count += 1

 print "Reading " + entry[0]

 text = urllib.urlopen(entry[1]).read()
 
 dom = BeautifulSoup(text)
 header = dom.find(text=re.compile("Product Description"))
 items = header.nextSibling.nextSibling.contents
 
 for l in range(1,len(items),6):
   title = items[l].h3.a.contents[0]
   if items[l].h3.contents[0] != items[l].h3.a:
     title = items[l].h3.contents[0] + title
   link = items[l].h3.a['href']
   out = re.compile(" ([0-9.]*)([MGT])B").findall(title)[0] # dropped terminal space in regex - avoids barfing on strings like " 16GB("
   size = float(out[0])
   if out[1] == 'T':
     size *= 1000
   if out[1] == 'M': # the unit is GB so adjust for sizes like 512MB
     size /= 1000
   price = float(items[l].find(text=re.compile("Your Price:")).split('$')[1].replace(',',''))
   myitems.append((size,price,title,link))
 
 maxl = [(x[0]/x[1],x) for x in myitems ] 
 maxl.sort()
 maxl.reverse()
 
 f.write("<h5>"+entry[0] + ":</h5>\n"); # Title section on best list
 for x in range(min(5, len(maxl))):
   f.write("<p>%i. (%f GB/$) <a href=\"%s\">%s</a> - $%s</p>\n" % (x+1 , maxl[x][0] , maxl[x][1][3] , maxl[x][1][2] , maxl[x][1][1]))

 g("set style line %d lc %d" % (count, count))

 # throw plot data into array for later plotting
 # (Should be able to say g.replot(...) instead and have the data added to replot.)
 plotdata.append( Gnuplot.Data([(x[0],x[0]/x[1]) for x in myitems ], **{'with':"points ls %d" % count, 'title':entry[0]}) )

# g.plot(plotdata) doesn't work, so eval a string in the form "g.plot(plotdata[0], plotdata[1], ... )"
eval("g.plot(" + ", ".join(["plotdata[%d]" % x for x in range(len(plotdata))]) + ")")
