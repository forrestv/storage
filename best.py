def best(myitems, outfile):
    maxl = []
    for x in myitems:
        maxl.append((x[0]/x[1],x))
    maxl.sort()
    maxl.reverse()
    
    f = open(outfile, "w")
    for i, (gbprice, item) in zip(range(10), maxl):
        s = u"<p>%i. (%f GB/$) <a href=\"%s\">%s</a> - $%s</p>\n" % (i+1, gbprice, item[3], item[2], item[1])
        f.write(s.encode("UTF-8"))
    return maxl[0][0] if maxl and maxl[0] else 0.

