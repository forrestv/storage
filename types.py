import os
import time

import newegg
import graph
import best

types = [
    ('sata', {None: (2010150014, '359:15133', '359:7918')}),
    ('satas', {None: (2010150380, '359:15133', '359:7918')}),
    ('usb', {None: (2013240522,)}),
    ('ssd', {None: (2010150636,)}),
    ('enclosure', {None: (2010150414, '359:20386', '359:15635', '359:47642', '359:28161', '359:28610', '359:32416', '359:7839', '359:7851', '360:7801', '360:7802')}),
]

result_dir = os.path.join(os.path.dirname(__file___), "result")

for name, subtypes in types:
    print name
    
    print 'Scraping'
    t = time.time()
    items = dict((subname, newegg.get(*call)) for subname, call in subtype.iteritems())
    
    print 'Graphing'
    graph.graph(items, os.path.join(result_dir, name + '.png'))
    
    print 'Itemizing'
    b = best.best(items, os.path.join(result_dir, name + '.txt'))
    
    record = name, t, b
    open(os.path.join(result_dir, 'record.txt'), 'a').write(repr(record) + "\n")
