# Author: Gregory Giuliani (Unversity of Geneva/EnviroSpace & UNEP/GRID-Geneva)
# http://www.unige.ch/envirospace
# http://www.grid.unep.ch
# 
# SWAT join WPS
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
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
                        identifier = "swat_join",
                        title = "SWAT Join",
                        version = "1.0",
                        storeSupported = "false",
                        statusSupported = "true",
                        grassLocation = True,
                        abstract = "Join DBF files with SWAT sub-basins shapefile")
		#Datainputs
		#DBF file		
		self.dbfFile = self.addLiteralInput(identifier="dbfFile", title="DBF File", abstract="DBF file in SWAT format", type=str)

		#SHP file
		self.shpFile = self.addLiteralInput(identifier="shpFile", title="Shape File", abstract="Subbasin shapefile", type=str)

		#Output
		self.shpOut = self.addLiteralOutput(identifier="shpOut",title="Output joined SHP file",type=str)

        def execute(self):
		#input shapefile in GRASS
		self.cmd(["v.in.ogr dsn=/home/greg/toto.shp output=mysoils"])
		
		#input DBF file in GRASS
		self.cmd(["db.in.ogr soils_legend.csv out=soils_legend"])

		#join DBF and SHP
		self.cmd(["v.db.join mysoils col=label otable=soils_legend ocol=shortname"])

		#write the joined SHP
		self.cmd(["v.out.ogr", "input=mysoils","format=ESRI_Shapefile","type=point","dsn=/var/www/wps/wpsoutputs/out.shp"])
		
		#Output SHP file
		self.shpOut.setValue("http://localhost/wps/wpsoutputs/"+random_string+"/output.zip")
                return
