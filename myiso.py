import isocronut
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
import gmplot
import sys

MAX_TRIES = 3
 
mapname = "intersection.html"
angles = 12

durations = [30,20,35]
methods = ['drive','drive','drive']
origins = ['10100 Santa Monica Blvd, Los Angeles','Santa Monica Pier','221 S Grand Ave, Los Angeles, CA 90012']



if len(durations) != len(origins):
	print "Mismatched durations and origins"
	sys.exit()
isos = []
for i in range(len(origins)):
	tries = 0
	failed = True
	while failed and tries < MAX_TRIES:
		tries += 1
		failed = False
		try:
			print "Generating isochrone {0} for {1} within {2} minutes {3}".format(i,origins[i],durations[i],methods[i])
			isos.append(isocronut.get_isochrone(origins[i],durations[i],angles,mode=methods[i]))
		except:
			failed = True
			print("Encountered error:", sys.exc_info()[0])
			print("Trying again")



for i in range(len(origins)):
	temp = gmplot.GoogleMapPlotter(isos[i][0][0],isos[i][0][1],14)
	temp .plot([item[0] for item in isos[i]],[item[1] for item in isos[i]],'cornflowerblue','edge_width=5')
	temp.draw("{0}.html".format(origins[i]))

print "Finding intersection"
cur = Polygon(isos[0])
for i in range(1,len(origins)):
	temp = Polygon(isos[i])
	cur = cur.intersection(temp)
if cur.is_empty:
	print "No intersection exists"
else:
	xs = []
	ys = []
	if type(cur) == MultiPolygon:
		for poly in cur.geoms:
			x,y = poly.exterior.coords.xy
			xs.append(x)
			ys.append(y)

	else:
		x,y = cur.exterior.coords.xy
		xs.append(x)
		ys.append(y)

	print "Plotting as {0}".format(mapname)
	gmap = gmplot.GoogleMapPlotter(xs[0][0],ys[0][0],14)

	for i in range(len(xs)):
		x,y = xs[i],ys[i]
		gmap.plot(x,y,'cornflowerblue',edge_width=5)
	
	gmap.draw(mapname)

	# simple1 = gmplot.GoogleMapPlotter(iso1[0][0],iso1[0][1],14)
	# simple1.plot([item[0] for item in iso1],[item[1] for item in iso1],'cornflowerblue',edge_width=5)
	# simple1.draw("a.html")

	# simple2 = gmplot.GoogleMapPlotter(iso2[0][0],iso2[0][1],14)
	# simple2.plot([item[0] for item in iso2],[item[1] for item in iso2],'cornflowerblue',edge_width=5)
	# simple2.draw("b.html")
