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
from getPaths import *


#############################


#############################################
# MAKE SURE YOU SET THE NECESSARY RAM
# MEMORY (MORE THAN 10G) IN THE FOLLOWING VARIABLES BEFORE CALLING THIS SCRIPT
# _JAVA_OPTIONS
# JAVA_TOOL_OPTIONS
# ##########################################

# Some definitions

outForm='GeoTIFF+XML'
WKTReader = snappy.jpy.get_type('com.vividsolutions.jts.io.WKTReader')
HashMap = snappy.jpy.get_type('java.util.HashMap')
SubsetOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
Point = snappy.jpy.get_type('java.awt.Point')
Dimension = snappy.jpy.get_type('java.awt.Dimension')
System = jpy.get_type('java.lang.System')
BandDescriptor = jpy.get_type('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor')


flist=listdir(sarIn)


f=flist[0]

product = ProductIO.readProduct(sarIn+"/"+f)

height = product.getSceneRasterHeight()
width = product.getSceneRasterWidth()
name = product.getName()
description = product.getDescription()
band_names = product.getBandNames()

GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

    # Subset into 4 pieces

size = product.getSceneRasterSize()

p_ul = Point(1000,0)

subsetDim = Dimension(size.width/6-1000,size.height/6)

r_ul = Rectangle(p_ul,subsetDim)

r=r_ul

op = SubsetOp()
op.setSourceProduct(product)
op.setCopyMetadata(True)
op.setRegion(r)
product_subset = op.getTargetProduct()
labelSubset = "x" + r.x.__str__() + "_y" + r.y.__str__()

proj = proj[0]
## Calibration

params = HashMap()
root = xml.etree.ElementTree.parse(home['parameters']+'calibration.xml').getroot()
for child in root:
    params.put(child.tag,child.text)

Cal = GPF.createProduct('Calibration',params,product_subset)

        ## Speckle filtering

params = HashMap()
root = xml.etree.ElementTree.parse(home['parameters']+'speckle_filtering.xml').getroot()
for child in root:
    params.put(child.tag,child.text)

CalSf = GPF.createProduct('Speckle-Filter',params,Cal)

        ## Band Arithmetics 1

expression = open(home['parameters']+'band_maths1.txt',"r").read()

targetBand1 = BandDescriptor()
targetBand1.name = 'watermask'
targetBand1.type = 'float32'
targetBand1.expression = expression

targetBands = jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 1)
targetBands[0] = targetBand1

parameters = HashMap()
parameters.put('targetBands', targetBands)
CalSfWater = GPF.createProduct('BandMaths', parameters, CalSf)

current_bands = CalSfWater.getBandNames()
print("Current Bands after Band Arithmetics 2:   %s \n" % (list(current_bands)))

### write output
ProductIO.writeProduct(CalSfWater,sarOut+"/testproduct_watermask",outForm)

### release products from memory
product_subset.dispose()
CalSf.dispose()
CalSfWater.dispose()
product.dispose()
System.gc()
