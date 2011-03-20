def best(name, type, outfile, t, recordfile):
    f = open(outfile, "w")
    for subname, items in type.iteritems():
        if subname:
            f.write((u"<h4>%s</h4>" % subname).encode("UTF-8"))
        
        maxl = []
        for x in items:
            maxl.append((x[0]/x[1],x))
        maxl.sort(reverse=True)
        
        for i, (gbprice, item) in zip(range(20), maxl):
            s = u"<p>%i. (%f GB/$) %s eggs (%s) <a href=\"%s\">%s</a> - $%s</p>\n" % (i+1, gbprice, item[5], item[4], item[3], item[2], item[1])
            f.write(s.encode("UTF-8"))
        
        record = name, subname, t, maxl[0][0] if maxl and maxl[0] else None
        open(recordfile, 'a').write(repr(record) + "\n")

