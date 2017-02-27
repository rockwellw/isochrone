import isocronut
from shapely.geometry import Polygon
import gmplot
import sys
 
mapname = "intersection.html"
angles = 10
durations = [15,20,15]
methods = ['walking','walking','driving']
origins = ['Toss Noodle Bar, Berkeley','University Hall, Berkeley','Indian Rock Park, Berkeley']



if len(durations) != len(origins):
	print "Mismatched durations and origins"
	sys.exit()
isos = []
for i in range(len(origins)):
	print "Generating isochrone {0} for {1} within {2} minutes {3}".format(i,origins[i],durations[i],methods[i])
	isos.append(isocronut.get_isochrone(origins[i],durations[i],angles,mode=methods[i]))


print "Finding intersection"
cur = Polygon(isos[0])
for i in range(1,len(origins)):
	temp = Polygon(isos[i])
	cur = cur.intersection(temp)
if cur.is_empty:
	print "No intersection exists"
else:
	x,y = cur.exterior.coords.xy

	print "Plotting as {0}".format(mapname)
	gmap = gmplot.GoogleMapPlotter(x[0],y[0],14)
	gmap.plot(x,y,'cornflowerblue',edge_width=5)
	gmap.draw(mapname)

	# simple1 = gmplot.GoogleMapPlotter(iso1[0][0],iso1[0][1],14)
	# simple1.plot([item[0] for item in iso1],[item[1] for item in iso1],'cornflowerblue',edge_width=5)
	# simple1.draw("a.html")

	# simple2 = gmplot.GoogleMapPlotter(iso2[0][0],iso2[0][1],14)
	# simple2.plot([item[0] for item in iso2],[item[1] for item in iso2],'cornflowerblue',edge_width=5)
	# simple2.draw("b.html")