import newegg
import graph
import best
import time

types = [
('SATA', (2010150014, '359:15133', '359:7918')),
('SATAs', (2010150380, '359:15133', '359:7918')),
('USB', (2013240522,)),
('SSD', (2010150636,)),
('enclosure', (2010150414, '359:20386', '359:15635', '359:47642', '359:28161', '359:28610', '359:32416', '359:7839', '359:7851', '360:7801', '360:7802')),
]

for type, call in types:
  print type
  type2 = type.replace(' ', '').lower()
  
  t = time.time()
  myitems = newegg.get(*call)
  
  print 'Scraping'
  myitems = list(myitems)
  
  print 'Graphing'
  graph.graph(myitems, None, 'result/'+type2+'.png')
  
  print 'Itemizing'
  b = best.best(myitems, 'result/'+type2+'.txt')
  open('record', 'a').write('%f %s %f' % (t, type, b))
