import os
import random
import time

import Gnuplot

def graph(myitems, out_name):
    tmp_name = out_name+".tmp"+str(random.randrange(2**24))
    g = Gnuplot.Gnuplot(debug=1)
    g("set terminal png size 1200,800 nocrop x000000 xA9A9A9 xA9A9A9 xFF0000 x00FF00 x0000FF")
    g("set border 3")
    g("set xtics 31556952")
    g("set ytics nomirror")
    g.set_string("output", tmp_name)
    g.xlabel('Time')
    g.ylabel('Max GB/$');
    g("set style line 1 lc 1")
    g("set style line 2 lc 2")
    g("set style line 3 lc 3")
    g("set style line 4 lc 4")
    l = []
    for i, (k, v) in enumerate(myitems):
        if v:
            params = {}
            params['with'] = "points ls %i" % (i+1)
            if k:
                params['title'] = k
            l.append(Gnuplot.Data(v, **params))
    g.plot(*l)
    while not os.path.exists(tmp_name):
        time.sleep(1)
    os.rename(tmp_name, out_name)

fixes = {
'enclosure 2.5"': 'enclosure 2.5 inch',
'enclosure 3.5"': 'enclosure 3.5 inch',
'enclosure 2.5in': 'enclosure 2.5 inch',
'enclosure 3.5in': 'enclosure 3.5 inch',
'ssd enterprise': 'ssd Enterprise',
'sata': 'hdd',
'satas': 'laptop_hdd',
'sata 3.5in': 'hdd',
'sata 2.5in': 'laptop_hdd',
'flash microSD': 'flash MicroSD',

'enclosure': 'enclosure 2.5 inch',
'ssd': 'ssd Normal',
}

data = {}
for line in open('result/record.txt'):
    line = eval(line)
    assert line[2] is not None
    if line[3] is None: continue
    if line[3] > 40: continue
    name = line[0].lower() + (' ' + line[1] if line[1] is not None else '')
    name = fixes.get(name, name)
    data.setdefault(name, []).append((line[2], line[3]))
for a, b in data.items():
    if len(b) < 100:
       data.pop(a)
    print a, (min(x[0] for x in b), max(x[0] for x in b)), (min(x[1] for x in b), max(x[1] for x in b))
graph(data.items(), "time.png")
