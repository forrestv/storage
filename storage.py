#!/usr/bin/env python
import os
import time

import best
import graph
import newegg

types = [
    ('hdd', [(None, (2010150014,))]),
    ('laptop_hdd', [(None, (2010150380,))]),
    ('flash', [
        ("SD", (2010170068, '531:7930',
         '531:25651', '531:57101', '531:17056')),
        ("MicroSD", (2010170068, '531:31144', '531:18914')),
        ("CF", (2010170068, '531:7923')),
    ]),
    ('usb', [(None, (2013240522,))]),
    ('ssd', [
        ('Normal', (dict(N=100008120, IsNodeId=1),)),
        ('External', (dict(N=100011690, IsNodeId=1),)),
        ('Enterprise', (dict(N=100011691, IsNodeId=1),)),
    ]),
    ('enclosure', [
        ('3.5 inch', (2010150414, '360:7800')),
        ('2.5 inch', (2010150414, '360:7801')),
    ]),
]

result_dir = os.path.join(os.path.dirname(__file__), "result")

for name, subtypes in types:
    t = time.time()

    print
    print name

    print 'Scraping'
    items = dict((subname, list(newegg.get(*call)))
                 for subname, call in subtypes)

    print 'Graphing'
    graph.graph([(subname, [(item[0], item[0] / item[1]) for item in items[subname]])
                for subname, call in subtypes], os.path.join(result_dir, name + '.png'))

    print 'Itemizing'
    best.best(name, [(subname, items[subname]) for subname, call in subtypes],
              os.path.join(result_dir, name + '.txt'), t, os.path.join(result_dir, 'record.txt'))
