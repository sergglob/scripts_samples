#!/usr/bin/python3.6
#Developed by Novikov Sergey (nose)
#TEMPLATE=json file with the geofences data, REDJPS platform
#
import  json, sys
def main ():
	file=sys.argv[1]
	if len(sys.argv)>1:
		print("Reading file")
		jf=rd(file)
		#########################################################v
		f= open("output.kml", "a")	#create output file
		print("<?xml version=\"1.0\" encoding=\"utf-8\"?>", file=f)
		print("<kml>", file=f)
		print("\t<Document>", file=f)
		print("\t\t<name>", file=f)
		print("\t\t\tGeofences", file=f)
		print("\t\t</name>", file=f)
		f.close()
		#########################################################
		poi=jf['markers']
		multi=jf['zones']
		if len(poi)>0:
			pois(poi)
		if len(multi)>0:
			multis(multi)

		#########################################################
		f= open("output.kml", "a")
		print("\t</Document>", file=f)
		print("</kml>", file=f)
		f.close()
		print("output.kml file is ready, saved in the same directory as a script placed!")
		print("Script work completed")
		#########################################################

	else:
		print("No file argument passed. Please launch the script with the file name './python.script file_name'")
		main()

def rd (fl):
	with open(fl,'r') as fi:
		ff=json.load(fi)
	return ff
def pois(p):
	for i in range(len(p)):
		name=p[i]['name']
		lat=p[i]['lat']
		lon=p[i]['lng']
		desc=p[i]['desc']
		#########################################################
		f= open("output.kml", "a")
		print("\t\t<Placemark>", file=f)	
		print("\t\t\t<name>", file=f)	
		print("\t\t\t\t",name, file=f)	
		print("\t\t\t</name>", file=f)	
		print("\t\t\t<description color=\"%s\" width=\"%s\">" % ('99307b19', 10.0), file=f)	#circle geofence color and radius
		print("\t\t\t\t",desc, file=f)		#description
		print("\t\t\t</description>", file=f)	
		print("\t\t\t<Point>", file=f)	
		print("\t\t\t\t<coordinates>", file=f)	
		print("\t\t\t\t\t%s,%s,0" % (lat, lon), file=f)		#coordinates lat, lon
		print("\t\t\t\t</coordinates>", file=f)	
		print("\t\t\t</Point>", file=f)	
		print("\t\t</Placemark>", file=f)	
		f.close()
		#########################################################
def multis(m):
	for j in range(len(m)):
		name=str(m[j]['name']).replace('&','&amp;')
		desc=''
		coor=''
		coordinates=str(m[j]['vertices'])	#string with the coordinates
		c1=coordinates.split(',')
		print(j+1,'  -- ###############   ',name,'   ###################')
#		print(c1)
		while len(c1)!=0:
			c3=c1[1]+','+c1[0]+',0 '
#			print(c3)
			coor=coor+c3
			c1=c1[2:]
#			print(coor)
		print(coor)
		print('##################################################################')
		color='990000ff'		#tr(m[j]['color']).replace('#','dd')
		width=50.0				#radius
		#########################################################
		f= open("output.kml", "a")
		print("\t\t<Placemark>", file=f)	
		print("\t\t\t<name>", file=f)	
		print("\t\t\t\t",name, file=f)	
		print("\t\t\t</name>", file=f)	
		print("\t\t\t<description>", file=f)
		print("\t\t\t\t",desc, file=f)		#description
		print("\t\t\t</description>", file=f)	
		#########################################################		
		if m[j]['area']!='':	#polygon
			print("\t\t\t<Style>", file=f)	
			print("\t\t\t\t<LineStyle>", file=f)	
			print("\t\t\t\t\t<color>", file=f)	
			print("\t\t\t\t\t\t",color, file=f)	
			print("\t\t\t\t\t</color>", file=f)	
			print("\t\t\t\t\t<width>", file=f)	
			print("\t\t\t\t\t\t",width, file=f)	
			print("\t\t\t\t\t</width>", file=f)	
			print("\t\t\t\t</LineStyle>", file=f)	
			print("\t\t\t\t<PolyStyle>", file=f)	
			print("\t\t\t\t\t<color>", file=f)	
			print("\t\t\t\t\t\t",color, file=f)	
			print("\t\t\t\t\t</color>", file=f)	
			print("\t\t\t\t</PolyStyle>", file=f)	
			print("\t\t\t</Style>", file=f)	
			print("\t\t\t<Polygon>", file=f)	
			print("\t\t\t\t<outerBoundaryIs>", file=f)	
			print("\t\t\t\t\t<LinearRing>", file=f)	
			print("\t\t\t\t\t\t<coordinates>", file=f)	
			print("\t\t\t\t\t\t\t",coor, file=f)	
			print("\t\t\t\t\t\t</coordinates>", file=f)	
			print("\t\t\t\t\t</LinearRing>", file=f)
			print("\t\t\t\t</outerBoundaryIs>", file=f)	
			print("\t\t\t</Polygon>", file=f)	

		else:
			print(name, " - error detecting area type")
			continue


		print("\t\t</Placemark>", file=f)	
		f.close()



main()
