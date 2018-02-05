
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

# Subset into one piece on the upper-left corner

size = product.getSceneRasterSize()

p_ul = Point(500,0)

subsetDim = Dimension(size.width/4-500,size.height/4)

r = Rectangle(p_ul,subsetDim)

##### process upper left only as an example

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

## Geometric correction

params = HashMap()
root = xml.etree.ElementTree.parse(proj+"/parameters/"+'terrain_correction2.xml').getroot()
for child in root:
    params.put(child.tag,child.text)
    
CalSfCorr = GPF.createProduct('Terrain-Correction',params,CalSf)


### write output
ProductIO.writeProduct(CalSfCorr,sarOut+"/"+product.getName() + "_" + labelSubset,outForm)

### release products from memory
product_subset.dispose()
CalSf.dispose()
CalSfCorr.dispose()
product.dispose()
System.gc()

