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
    ('flash', {
        "SD": (2010170068, '531:17056', '531:7930', '531:25651'),
        "miniSD": (2010170068, '531:25687', '531:14916'),
        "microSD": (2010170068, '531:31144', '531:18914'),
        "CF": (2010170068, '531:7923'),
    }),
]

result_dir = os.path.join(os.path.dirname(__file__), "result")

for name, subtypes in types:
    t = time.time()
    
    print
    print name
    
    print 'Scraping'
    items = dict((subname, list(newegg.get(*call))) for subname, call in subtypes.iteritems())
    
    print 'Graphing'
    graph.graph(dict((k, [(item[0], item[0]/item[1]) for item in v]) for k, v in items.iteritems()), os.path.join(result_dir, name + '.png'))
    
    print 'Itemizing'
    best.best(name, items, os.path.join(result_dir, name + '.txt'), t, os.path.join(result_dir, 'record.txt'))
