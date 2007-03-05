#!/usr/bin/python

import csv
import sys

def hl():
    print "=" * 80


hl()

dir = sys.argv[1]
gpsfile = dir + '/gps.log'
eventfile = dir + '/event.log'

f = open(sys.argv[2],'w')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<kml xmlns="http://earth.google.com/kml/2.0">\n')
f.write('<Document>\n')
f.write('<name>NetCar GPRSping</name>\n')
f.write('<visibility>1</visibility>\n')
f.write("""
   <Style id="start">
      <IconStyle>
         <color>ff00ff00</color>
         <colorMode>normal</colorMode>
         <scale>1.0</scale>
      </IconStyle>
   </Style>
   <Style id="stop">
      <IconStyle>
         <color>ff0000ff</color>
         <colorMode>normal</colorMode>
         <scale>1.0</scale>
      </IconStyle>
   </Style>
   <Style id="left">
      <IconStyle>
         <color>ffff0000</color>
         <colorMode>normal</colorMode>
         <scale>1.0</scale>
      </IconStyle>
   </Style>
   <Style id="right">
      <IconStyle>
         <color>ffaaaa00</color>
         <colorMode>normal</colorMode>
         <scale>1.0</scale>
      </IconStyle>
   </Style>
   <Style id="rouff">
      <IconStyle>
         <color>ff00aaaa</color>
         <colorMode>normal</colorMode>
         <scale>1.0</scale>
      </IconStyle>
   </Style>
   <Style id="speed">
      <IconStyle>
         <color>ff0aa00a</color>
         <colorMode>normal</colorMode>
         <scale>1.0</scale>
      </IconStyle>
   </Style>
   <Style id="speedbump">
      <IconStyle>
         <color>ffa0a00a</color>
         <colorMode>normal</colorMode>
         <scale>1.0</scale>
      </IconStyle>
   </Style>

""")
rawevents = file(eventfile).readlines()[1:]
events = {}
for e in rawevents:
    e = e.strip().split('\t')

    if len(e) <= 1:
        continue
    events[float(e[0])] = e[1]

oldlat = 0
oldlon = 0
for line in file(gpsfile).readlines()[1:]: 
    d = line.strip().split('\t')
    if len(d) >= 8 :
        nodeTime, lat, lon, alt, UTC, speed, satellites, pdop = d[0:8]
        if int(satellites) < 3 or (oldlat==lat and oldlon==lon):
            continue
        oldlat = lat
        oldlon = lon
        nodeTime = float(nodeTime)    
        
        found = 0 
        for k in events.keys():
            if abs(nodeTime-k) < 4:
                found = 1
                break
                            
        try:
	    f.write('\t\t<Placemark>\n')
	    f.write('\t\t\t<name></name>\n')
	    f.write('\t\t\t<description>Time: %s<br /> Altitude: %s m<br /> Speed: %s <br /> satellites %s ' %(nodeTime, alt, speed, satellites))
            if found:
                f.write('<br />Event: %s</description>\n'%(events[k],))
                f.write('\t\t\t<styleUrl>#%s</styleUrl>\n'%(events[k].split()[1],))
            else:
                f.write('</description>\n')
	    f.write('\t\t\t<View>\n')
	    f.write('\t\t\t\t<longitude>%s</longitude>\n' % lon)
	    f.write('\t\t\t\t<latitude>%s</latitude>\n' % lat)
	    f.write('\t\t\t</View>\n')
	    f.write('\t\t\t<visibility>1</visibility>\n')
	    #f.write('\t\t\t<styleUrl>root://styleMaps#default?iconId=0x307</styleUrl>\n')
	    f.write('\t\t\t<Point><coordinates>%s,%s,45</coordinates></Point>\n' % (lon, lat) )
	    f.write('\t\t</Placemark>\n')

        except e:
	    print e
    
f.write('</Document>\n')
f.write('</kml>')
hl()    

