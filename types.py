import time

import newegg
import graph
import best

types = [
    ('sata', (2010150014, '359:15133', '359:7918')),
    ('satas', (2010150380, '359:15133', '359:7918')),
    ('usb', (2013240522,)),
    ('ssd', (2010150636,)),
    ('enclosure', (2010150414, '359:20386', '359:15635', '359:47642', '359:28161', '359:28610', '359:32416', '359:7839', '359:7851', '360:7801', '360:7802')),
]

for type, call in types:
    print type
    
    myitems = newegg.get(*call)
    
    print 'Scraping'
    t = time.time()
    myitems = list(myitems)
    
    print 'Graphing'
    graph.graph(myitems, None, 'result/' + type + '.png')
    
    print 'Itemizing'
    b = best.best(myitems, 'result/' + type + '.txt')
    open('record', 'a').write('%s %f %f\n' % (type, t, b))
