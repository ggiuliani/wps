# Author: Gregory Giuliani (Unversity of Geneva/EnviroSpace & UNEP/GRID-Geneva)
# http://www.unige.ch/envirospace
# http://www.grid.unep.ch
# 
# USHAHIDI converter WPS
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

import os,sys,string
from pywps.Process.Process import WPSProcess
class Process(WPSProcess):
	def __init__(self):
		WPSProcess.__init__(self,
        		identifier = "ushahidi2shp",
            		title = "Ushahidi converter",
                	version = "1.0",
                	storeSupported = "false",
                	statusSupported = "true",
                	grassLocation = True,
                	abstract = "Convert Ushahidi data to shapefile")
		#Datainputs
		#Ushahidi KML URL		
		self.ushahidiKmlUrl = self.addLiteralInput(identifier="ushahidiKmlUrl",title="Ushahidi KML interface URL", abstract="URL to the KML service of Ushahidi (install related plugin if needed)", type=str)

		#Output
		self.shpOut = self.addLiteralOutput(identifier="shpOut",title="Output SHP file",type=str)

        def execute(self):
		#Download and write KML file from Ushahidi endpoint
		os.system("curl -o /var/www/wps/wpsoutputs/ushahidi.kml "+self.getInputValue('ushahidiKmlUrl'))
		
		#Convert KML to SHP
		os.system('ogr2ogr -f "ESRI Shapefile" /var/www/wps/wpsoutputs/ushahidi.shp /var/www/wps/wpsoutputs/ushahidi.kml')
		
		#Output SHP file
		os.chdir("/var/www/wps/wpsoutputs/")
		os.system("zip output.zip ushahidi.shp ushahidi.shx ushahidi.dbf")
		self.shpOut.setValue("http://localhost/wps/wpsoutputs/output.zip")
        	return
