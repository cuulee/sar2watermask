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


from modules.getPaths import *


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

product = ProductIO.readProduct(sarOut+"/testproduct_watermask.tif")

height = product.getSceneRasterHeight()
width = product.getSceneRasterWidth()
name = product.getName()
description = product.getDescription()
band_names = product.getBandNames()

GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

## Geometric correction

params = HashMap()
root = xml.etree.ElementTree.parse(proj+"/parameters/"+'terrain_correction.xml').getroot()
for child in root:
    params.put(child.tag,child.text)

CalSfWaterCorr1 = GPF.createProduct('Terrain-Correction',params,CalSfWater)

current_bands = CalSfWaterCorr1.getBandNames()
print("Current Bands after Terrain Correction:   %s \n" % (list(current_bands)))



        ### write output
ProductIO.writeProduct(CalSfWaterCorr2,sarOut+"/"+product.getName() + "_" + labelSubset + "_watermask",outForm)

        ### release products from memory
product_subset.dispose()
CalSf.dispose()
CalSfWater.dispose()
CalSfWaterCorr1.dispose()
product.dispose()
System.gc()
