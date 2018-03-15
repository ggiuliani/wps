# Author: Gregory Giuliani (Unversity of Geneva/EnviroSpace & UNEP/GRID-Geneva)
# http://www.unige.ch/envirospace
# http://www.grid.unep.ch
# 
# SWAT extractor WPS
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
                        identifier = "swat_extractor",
                        title = "SWAT extractor",
                        version = "1.0",
                        storeSupported = "false",
                        statusSupported = "true",
                        grassLocation = True,
                        abstract = "Download module to setup a SWAT model (Rivers, DEM, Soils, Land Use, Temperatures, Precipitations). Data will be in WGS84")
		#Datainputs		
		#Bounding Box		
		self.northBound = self.addLiteralInput(identifier="northBound", title="North", abstract="North bounding [decimal degrees]", type=str)
		self.southBound = self.addLiteralInput(identifier="southBound", title="South", abstract="South bounding [decimal degrees]", type=str)
		self.eastBound = self.addLiteralInput(identifier="eastBound", title="East", abstract="East bounding [decimal degrees]", type=str)
		self.westBound = self.addLiteralInput(identifier="westBound", title="West", abstract="West bounding [decimal degrees]", type=str)                
		
		#Rivers
		self.riversInUrl = self.addLiteralInput(identifier="riversInUrl",title="Rivers WFS endpoint", abstract="WFS URL giving access to river data set", type=str)
        	self.riversInLayerName = self.addLiteralInput(identifier="riversInLayerName",title="Rivers layername", abstract="Name of the river WFS layer", type=str)
		
		#DEM
		self.demInUrl = self.addLiteralInput(identifier="demInUrl",title="DEM WCS endpoint", abstract="WCS URL giving access to DEM data set", type=str)
		self.demInLayerName = self.addLiteralInput(identifier="demInLayerName",title="DEM layername", abstract="Name of the DEM WCS layer", type=str)
		
		#Soils		
		self.soilsInUrl = self.addLiteralInput(identifier="soilsInUrl",title="Soils WCS endpoint", abstract="WCS URL giving access to soils data set", type=str)
		self.soilsInLayerName = self.addLiteralInput(identifier="soilsInLayerName",title="Soils layername", abstract="Name of the soils WCS layer", type=str)
		
		#Land Use
		self.landuseInUrl = self.addLiteralInput(identifier="landuseInUrl",title="Land Use WCS endpoint", abstract="WCS URL giving access to land use data set", type=str)
		self.landuseInLayerName = self.addLiteralInput(identifier="landuseInLayerName",title="LandUse layername", abstract="Name of the land use WCS layer", type=str)
		
		#Temperatures		
		self.tempInUrl = self.addLiteralInput(identifier="tempInUrl",title="Temperatures WFS endpoint", abstract="WFS URL giving access to temperatures data set", type=str)
        	self.tempInLayerName = self.addLiteralInput(identifier="tempInLayerName",title="Temperatures layername", abstract="Name of the temperatures WFS layer", type=str)
		
		#Precipitations
		self.precipInUrl = self.addLiteralInput(identifier="precipInUrl",title="Precipitations WFS endpoint", abstract="WFS URL giving access to precipitations data set", type=str)
        	self.precipInLayerName = self.addLiteralInput(identifier="precipInLayerName",title="Precipitations layername", abstract="Name of the precipitations WFS layer", type=str)

		#Output
		self.swatOut = self.addLiteralOutput(identifier="swatOut",title="Output zip file",type=str)

        def execute(self):
		#Create a random folder name within wpsoutputs		
		random_string = "".join(random.sample(string.letters+string.digits, 20))
		os.system("mkdir /var/www/wps/wpsoutputs/"+random_string)		
		
		#Rivers
		self.cmd(["v.in.ogr","-o","dsn="+self.getInputValue('riversInUrl')+"service=WFS&version=1.0.0&request=GetFeature&typename="+self.getInputValue('riversInLayerName')+"&outputFormat=JSON&srs=EPSG:4326&bbox="+self.getInputValue('westBound')+","+self.getInputValue('southBound')+","+self.getInputValue('eastBound')+","+self.getInputValue('northBound')+"","output=riversInXml"])
		self.cmd(["v.out.ogr", "input=riversInXml","format=ESRI_Shapefile","type=line","dsn=/var/www/wps/wpsoutputs/"+random_string+"/rivers.shp"])

		#DEM
		os.system("wget -O /var/www/wps/wpsoutputs/"+random_string+"/dem.tif '"+self.getInputValue('demInUrl')+"service=WCS&version=1.0.0&request=GetCoverage&coverage="+self.getInputValue('demInLayerName')+"&Format=GeoTiff&width=640&height=309&crs=EPSG:4326&bbox="+self.getInputValue('westBound')+","+self.getInputValue('southBound')+","+self.getInputValue('eastBound')+","+self.getInputValue('northBound')+"'")
		
		#Soils
		os.system("wget -O /var/www/wps/wpsoutputs/"+random_string+"/soils.tif '"+self.getInputValue('soilsInUrl')+"service=WCS&version=1.0.0&request=GetCoverage&coverage="+self.getInputValue('soilsInLayerName')+"&Format=GeoTiff&resx=0.003&resy=0.003&crs=EPSG:4326&bbox="+self.getInputValue('westBound')+","+self.getInputValue('southBound')+","+self.getInputValue('eastBound')+","+self.getInputValue('northBound')+"'")

		#Land Use
		os.system("wget -O /var/www/wps/wpsoutputs/"+random_string+"/landuse.tif '"+self.getInputValue('landuseInUrl')+"service=WCS&version=1.0.0&request=GetCoverage&coverage="+self.getInputValue('landuseInLayerName')+"&Format=GeoTiff&width=640&height=309&crs=EPSG:4326&bbox="+self.getInputValue('westBound')+","+self.getInputValue('southBound')+","+self.getInputValue('eastBound')+","+self.getInputValue('northBound')+"'")

		#Temperatures
		self.cmd(["v.in.ogr","-o","dsn="+self.getInputValue('tempInUrl')+"service=WFS&version=1.0.0&request=GetFeature&typename="+self.getInputValue('tempInLayerName')+"&outputFormat=JSON&srs=EPSG:4326&bbox="+self.getInputValue('westBound')+","+self.getInputValue('southBound')+","+self.getInputValue('eastBound')+","+self.getInputValue('northBound')+"","output=tempInXml"])
		self.cmd(["v.out.ogr", "input=tempInXml","format=ESRI_Shapefile","type=point","dsn=/var/www/wps/wpsoutputs/"+random_string+"/temperatures.shp"])

		#Precipitations
		self.cmd(["v.in.ogr","-o","dsn="+self.getInputValue('precipInUrl')+"service=WFS&version=1.0.0&request=GetFeature&typename="+self.getInputValue('precipInLayerName')+"&outputFormat=JSON&srs=EPSG:4326&bbox="+self.getInputValue('westBound')+","+self.getInputValue('southBound')+","+self.getInputValue('eastBound')+","+self.getInputValue('northBound')+"","output=precipInXml"])
		self.cmd(["v.out.ogr", "input=precipInXml","format=ESRI_Shapefile","type=point","dsn=/var/www/wps/wpsoutputs/"+random_string+"/precipitations.shp"])
		
		#Output zip file
		os.chdir("/var/www/wps/wpsoutputs/"+random_string+"/")
		os.system("zip output.zip rivers.shp rivers.shx rivers.dbf dem.tif soils.tif landuse.tif temperatures.shp temperatures.dbf temperatures.shx precipitations.shp precipitations.dbf precipitations.shx")
		self.swatOut.setValue("http://localhost/wps/wpsoutputs/"+random_string+"/output.zip")
                return
