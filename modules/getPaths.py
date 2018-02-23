from os.path import expanduser
import sys


if expanduser("~")=='/home/delgado':
    home = {
        'home' : expanduser("~"),
        'auxdata' : expanduser("~") + '/proj/sar2watermask/auxdata',
        'parameters' : expanduser("~") + '/proj/sar2watermask/parameters'
    }

    home['scratch'] = expanduser("~") + '/scratch'
    home['proj'] = expanduser("~") + '/proj/buhayra/sar2watermask',
else:
    home = {
        'home' : expanduser("~"),
        'auxdata' : expanduser("~") + '/proj/tests/sar2watermask/auxdata',
        'parameters' : expanduser("~") + '/proj/tests/sar2watermask/parameters'
    }

    home['scratch'] = '/mnt/scratch/martinsd'
    home['proj'] = expanduser("~") + '/proj/tests/sar2watermask',


pyt = home['home'] + "/local/miniconda2/envs/gdal/bin/python"
gdalPol = home['home'] + "/local/miniconda2/envs/gdal/bin/gdal_polygonize.py"
gdalMerge = home['home'] + "/local/miniconda2/envs/gdal/bin/gdal_merge.py"
proj = home['proj']
scratch= home['scratch']


sardir=scratch+"/test_dataset/s1a_scenes"
sarIn=sardir+"/in"
sarOut=sardir+"/out"
polOut=scratch + "/test_dataset/watermasks"

MONGO_HOST = "141.89.96.184"
MONGO_DB = "sar2watermask"
MONGO_PORT = 27017

sys.path.insert(0, home['parameters'])
from parameters.credentials import *
