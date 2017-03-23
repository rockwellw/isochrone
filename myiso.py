import isocronut
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
import gmplot
import sys
from tempfile import mkstemp
from shutil import move
from os import remove, close

INCLUDE_API = True

MAX_TRIES = 3
DRAW_API = "AIzaSyCViPeu32mSIsvoGaSMXzMdm4mgWeOYEws"
mapname = "index.html"
angles = 20

durations = [30,20,35]
methods = ['drive','drive','drive']
origins = ['10100 Santa Monica Blvd, Los Angeles','Santa Monica Pier','221 S Grand Ave, Los Angeles, CA 90012']
durations = durations[:1]
methods = methods[:1]
origins = origins[:1]



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
	temp.plot([item[0] for item in isos[i]],[item[1] for item in isos[i]],'cornflowerblue',edge_width=5)
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

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

if INCLUDE_API:
	replace(mapname,"=true_or_false","=true_or_false&key=" + DRAW_API)


