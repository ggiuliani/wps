# Author: Gregory Giuliani (Unversity of Geneva/EnviroSpace & UNEP/GRID-Geneva)
# http://www.unige.ch/envirospace
# http://www.grid.unep.ch
# 
# SWAT output.sub processor WPS
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
                        identifier = "swat_outputsub_processor",
                        title = "SWAT outputsub processor",
                        version = "1.0",
                        storeSupported = "false",
                        statusSupported = "true",
                        grassLocation = True,
                        abstract = "Process SWAT output.sub file and creates a dbf file for each variable")
		#Datainputs		
		#output.sub file path		
		self.outputSub = self.addLiteralInput(identifier="outputSub", title="Output.sub file", abstract="Path to the output.sub file", type=str)  
		
		#output.sub file path		
		self.legendCsv = self.addLiteralInput(identifier="legendCsv", title="Legend.csv file", abstract="Path to the legend.csv file", type=str)
	
	def execute(self):
		import rpy2.robjects as robjects		
		sys.stdout=open("/dev/null","w") #import for verbose nature of R, can raise an http 500 error
		robjects.r('library(foreign)')
		robjects.r('Qs1<-read.table("/home/greg/Desktop/output.sub",skip=9)')	

		robjects.r('textfile<-readLines(file("/home/greg/Desktop/output.sub"))')
		robjects.r('write.dbf(textfile[9],"legend.dbf")')

		robjects.r('legend_names<-read.table("/home/greg/Desktop/legend.csv",sep=",")')
		
		for i in range(5, 25):			
			robjects.r('datafile<-Qs1[,c(2,%i)]' % i)
			robjects.r('colnames(datafile)=c(as.character(legend_names[1,1]),as.character(legend_names[1,%i]))' % i)
			robjects.r('write.dbf(datafile,paste("/var/www/wps/wpsoutputs/",substr(legend_names[1,%i], 1, 5),".dbf",sep=""))' % i)	
		sys.stdout=sys.__stdout__ #import for verbose nature of R, can raise an http 500 error	
		return
