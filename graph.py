import os
import random
import time

import Gnuplot

def graph(myitems, title, out_name):
  tmp_name = out_name+".tmp"+str(random.randrange(2**24))
  g = Gnuplot.Gnuplot(debug=1)
  g("set terminal png size 600,400 nocrop x000000 xFFFFFF xFFFFFF xFF0000 x00FF00 x0000FF")
  g("set border 3")
  g("set xtics nomirror")
  g("set ytics nomirror")
  g.set_string("output", tmp_name)
  if title:
      g.title(title)
  g.xlabel('Size in GB')
  g.ylabel('GB/$');
  g("set style line 1 lc 1")
  g("set style line 2 lc 2")
  g("set style line 3 lc 3")
  l = []
  ll = [
      ([(x[0],x[0]/x[1]) for x in myitems if x[2][0:4] != "Open" and x[2][-3:] != "OEM"], 'Retail'),
      ([(x[0],x[0]/x[1]) for x in myitems if x[2][0:4] != "Open" and x[2][-3:] == "OEM"], 'OEM'),
      ([(x[0],x[0]/x[1]) for x in myitems if x[2][0:4] == "Open"], 'Open'),
  ]
  for i, (d,title) in enumerate(ll):
    if d:
      l.append(Gnuplot.Data(d, **{'with':"points ls %i"%(i+1), 'title':title}))
  g.plot(*l)
  while not os.path.exists(tmp_name):
     time.sleep(1)
  os.rename(tmp_name, out_name)

