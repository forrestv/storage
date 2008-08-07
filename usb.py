import Gnuplot
import newegg

myitems = newegg.get(2013240522)

myitems = list(myitems)

g = Gnuplot.Gnuplot(debug=1)
g("set terminal png size 600,400 nocrop x000000 xFFFFFF xFFFFFF xFF0000 x00FF00 x0000FF")
g("set border 3")
g("set xtics nomirror")
g("set ytics nomirror")
g.set_string("output","sata2.png")
g.title('SATA 3.0Gbs Harddrives')
g.xlabel('Size in GB')
g.ylabel('GB/$');
g("set style line 1 lc 1")
g("set style line 2 lc 2")
g("set style line 3 lc 3")

d = [(x[0],x[0]/x[1]) for x in myitems if x[2][0:4] != "Open" and x[2][-3:] != "OEM"]
i = Gnuplot.Data(d, with="points ls 1", title = "Retail")
j = Gnuplot.Data([(x[0],x[0]/x[1]) for x in myitems if x[2][0:4] != "Open" and x[2][-3:] == "OEM"], with="points ls 2", title = "OEM")
k = Gnuplot.Data([(x[0],x[0]/x[1]) for x in myitems if x[2][0:4] == "Open"], with="points ls 3", title = "Open")
g.plot(i,j,k)

