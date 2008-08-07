def best(myitems, outfile):
  maxl = []
  for x in myitems:
    maxl.append((x[0]/x[1],x))
    print x
  maxl.sort()
  maxl.reverse()
  
  f = open(outfile, "w")
  for x in range(10):
    f.write("<p>%i. (%f GB/$) <a href=\"%s\">%s</a> - $%s</p>\n" % (x+1,maxl[x][0],maxl[x][1][3],maxl[x][1][2].decode('UTF-8'),maxl[x][1][1]))

