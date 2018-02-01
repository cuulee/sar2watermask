
from os import listdir
import os
import datetime
import sys
import numpy
import xml.etree.ElementTree
import snappy
from snappy import Product
from snappy import ProductData
from snappy import ProductUtils
from snappy import FlagCoding
from snappy import GPF
from snappy import ProductIO
from snappy import jpy
from snappy import HashMap
from snappy import Rectangle
from getPaths_testmode import *

#############################################
# MAKE SURE YOU SET THE NECESSARY RAM
# MEMORY (MORE THAN 10G) IN THE FOLLOWING VARIABLES BEFORE CALLING THIS SCRIPT
# _JAVA_OPTIONS
# JAVA_TOOL_OPTIONS
# ##########################################

# Some definitions

t0=datetime.datetime.now()


outForm='GeoTIFF+XML'
WKTReader = snappy.jpy.get_type('com.vividsolutions.jts.io.WKTReader')
HashMap = snappy.jpy.get_type('java.util.HashMap')
SubsetOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
Point = snappy.jpy.get_type('java.awt.Point')
Dimension = snappy.jpy.get_type('java.awt.Dimension')
System = jpy.get_type('java.lang.System')
BandDescriptor = jpy.get_type('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor')


flist=listdir(sarIn)
f = flist[0]

# Read product

product = ProductIO.readProduct(sarIn+"/"+f)
print("\n processing " + f + "\n")
print("at " + str(datetime.datetime.now()) + "\n")

# Obtain some attributes

height = product.getSceneRasterHeight()
width = product.getSceneRasterWidth()
name = product.getName()
description = product.getDescription()
band_names = product.getBandNames()

# Initiate processing
    
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

# Subset into 4 pieces

size = product.getSceneRasterSize()

p_ul = Point(500,0)
p_ur = Point(size.width/2,0)
p_ll = Point(500,size.height/2)
p_lr = Point(size.width/2,size.height/2)

subsetDim = Dimension(size.width/4-500,size.height/4)

r_ul = Rectangle(p_ul,subsetDim)
r_ur = Rectangle(p_ur,subsetDim)
r_ll = Rectangle(p_ll,subsetDim)
r_lr = Rectangle(p_lr,subsetDim)

rect=[r_ul,r_ur,r_ll,r_lr]

##### process upper left only as an example
r=r_ul

op = SubsetOp()
op.setSourceProduct(product)
op.setCopyMetadata(True)
op.setRegion(r)
product_subset = op.getTargetProduct()
labelSubset = "x" + r.x.__str__() + "_y" + r.y.__str__()


## Calibration
        
params = HashMap()

root = xml.etree.ElementTree.parse(proj+"/parameters/"+'calibration.xml').getroot()
for child in root:
    params.put(child.tag,child.text)
    
Cal = GPF.createProduct('Calibration',params,product_subset)
    
## Speckle filtering

params = HashMap()
root = xml.etree.ElementTree.parse(proj+"/parameters/"+'speckle_filtering.xml').getroot()
for child in root:
    params.put(child.tag,child.text)

CalSf = GPF.createProduct('Speckle-Filter',params,Cal)

### write output
ProductIO.writeProduct(CalSf,sarOut+"/"+product.getName() + "_" + labelSubset,outForm)

### release products from memory
product_subset.dispose()
CalSf.dispose()
product.dispose()
System.gc()

print("\n********** sar2watermask completed!" + str(len(flist))  + " scenes processed\n********** Elapsed time: " + str(datetime.datetime.now()-t0) + "\n********** End of message\n")
