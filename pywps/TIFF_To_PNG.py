from pywps.Process import WPSProcess

class TiffToPNG(WPSProcess):

    def __init__(self):
        WPSProcess.__init__(self,
            identifier = "TiffToPNG",
            title="TIFF to PNG",
            version = "1.0",
            storeSupported = True,
            statusSupported = True,
            abstract = "Conversion of a 3-band TIFF file to PNG",
            grassLocation = True)
      
        self.inputTIFF=self.addComplexInput(identifier='input',maxmegabites=100,title="input image",minOccurs=1,maxOccurs=1,formats = [{'mimeType': 'image/tiff'}, {'mimeType': 'image/geotiff'}, {'mimeType': 'application/geotiff'}, {'mimeType': 'application/x-geotiff'}])
        self.outputPNG=self.addComplexOutput(identifier="output",title="output PNG",formats=[{'mimeType':'image/png'}])
        
    def execute(self):
        self.cmd(["r.in.gdal","input=%s" % self.inputTIFF.getValue(),'output=inputTIFF','-o'])
        self.cmd(["r.composite","red=inputTIFF.red","green=inputTIFF.green","blue=inputTIFF.blue","output=inputTIFF"])
        self.cmd(["r.out.png","input=inputTIFF","output=./tmp.png"])
        self.outputPNG.setValue("./tmp.png")
	return
