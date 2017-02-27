import isocronut
from shapely.geometry import Polygon
import gmplot
import sys
 
mapname = "intersection.html"
angles = 8
durations = [10,7,7]
#origins = ['559 Nathan Abbott Way, Stanford, CA','160 San Gabriel Drive, Sunnyvale, CA']
origins = ['2430 Piedmont Ave, Berkeley, CA','2555 Benvenue Ave, Berkeley, CA','2977 College Ave, Berkeley, CA']



if len(durations) != len(origins):
	print "Mismatched durations and origins"
	sys.exit()
isos = []
for i in range(len(origins)):
	print "Generating isochrone {0} for {1} with duration {2}".format(i,origins[i],durations[i])
	isos.append(isocronut.generate_isochrone_map(origins[i],durations[i],angles))


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