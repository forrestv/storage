import newegg
import graph
import best

types = [
('SATA', (2010150014, '359:15133', '359:7918')),
('SATAs', (2010150380, '359:15133', '359:7918')),
('USB', (2013240522,))
]

for type, call in types:
  print type
  type2 = type.replace(' ', '').lower()
  
  myitems = newegg.get(*call)
  
  print 'Scraping'
  myitems = list(myitems)
  
  print 'Graphing'
  graph.graph(myitems, None, 'result/'+type2+'.png')
  
  print 'Itemizing'
  best.best(myitems, 'result/'+type2+'.txt')
