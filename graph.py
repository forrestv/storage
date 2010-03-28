import os
import random
import time

import Gnuplot

def graph(myitems, out_name):
  tmp_name = out_name+".tmp"+str(random.randrange(2**24))
  g = Gnuplot.Gnuplot(debug=1)
  g("set terminal png size 600,400 nocrop x000000 xFFFFFF xFFFFFF xFF0000 x00FF00 x0000FF")
  g("set border 3")
  g("set xtics nomirror")
  g("set ytics nomirror")
  g.set_string("output", tmp_name)
  g.xlabel('Size in GB')
  g.ylabel('GB/$');
  g("set style line 1 lc 1")
  g("set style line 2 lc 2")
  g("set style line 3 lc 3")
  g("set style line 4 lc 4")
  l = []
  for i, (k, v) in enumerate(myitems.iteritems()):
    if v:
      l.append(Gnuplot.Data(v, **{'with':"points ls %i"%(i+1), 'title':k}))
  g.plot(*l)
  while not os.path.exists(tmp_name):
     time.sleep(1)
  os.rename(tmp_name, out_name)

