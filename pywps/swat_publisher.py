# Author: Gregory Giuliani (Unversity of Geneva/EnviroSpace & UNEP/GRID-Geneva)
# http://www.unige.ch/envirospace
# http://www.grid.unep.ch
# 
# SWAT publisher WPS
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os,sys,string,random
from pywps.Process.Process import WPSProcess
class Process(WPSProcess):
        def __init__(self):
                WPSProcess.__init__(self,
                        identifier = "swat_publisher",
                        title = "SWAT Publisher",
                        version = "1.0",
                        storeSupported = "false",
                        statusSupported = "true",
                        grassLocation = True,
                        abstract = "Publish SWAT outputs maps in GeoServer")
		#Datainputs

		#Output
		self.shpOut = self.addLiteralOutput(identifier="shpOut",title="Output joined SHP file",type=str)

        def execute(self):
		#Add a new workspace
		os.system("curl -u admin:geoserver -v -XPOST -H 'Content-type: text/xml' -d '<workspace><name>acme</name></workspace>' http://localhost:8080/geoserver/rest/workspaces")

		#Add a new datastore
		os.system("curl -u admin:geoserver -v -XPOST -H 'Content-type: text/xml' -d '<coverageStore><name>wsgeotiff_imageGeoTiffWGS84_1298678792699</name><enabled>true</enabled><type>GeoTIFF</type><url>/home/gis/image_wgs84.tif</url>	</coverageStore>' http://localhost:8080/geoserver/rest/workspaces/acme/coveragestores")
		 
		#Upload the shapefile
		os.system("curl -u admin:geoserver -XPUT -H 'Content-type: text/plain' --data-binary @roads.zip http://localhost:8080/geoserver/rest/workspaces/acme/datastores/roads/file.shp")

		#Output SHP file
		self.shpOut.setValue("http://localhost/wps/wpsoutputs/"+random_string+"/output.zip")
                return
'''
curl -u admin:geoserver -v -XPOST -H 'Content-type: text/xml' \
      -d '<coverage>
          <name>imageGeoTiffWGS84</name>
          <title>imageGeoTiffWGS84</title>
          <nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS>
          <srs>EPSG:4326</srs>
          <latLonBoundingBox><minx>-179.958</minx><maxx>-105.002</maxx><miny>-65.007</miny><maxy>65.007</maxy><crs>EPSG:4326</crs></latLonBoundingBox>
          </coverage>' \
      "http://localhost:8080/geoserver/rest/workspaces/wsgeotiff/coveragestores/wsgeotiff_imageGeoTiffWGS84_1298678792699/coverages"
'''
