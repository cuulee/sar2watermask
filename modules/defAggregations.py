from pymongo import MongoClient
import json
import os
import sys 
from datetime import datetime,timedelta

def getLatestPolys(s2w):
    pipeline = [
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]

    aggrLatest=list(s2w.aggregate(pipeline=pipeline))
    
    latest=list()
    
    for feat in aggrLatest:
        poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']})
        latest.append(poly[0])
    return(latest)

def getLatestIngestionTime(s2w):
    pipeline = [
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]

    aggrLatest=list(s2w.aggregate(pipeline=pipeline))
    latest=list()
    
    for feat in aggrLatest:
        poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']},{'properties.id_cogerh' : 1,'properties.ingestion_time' : 1})
        latest.append(poly[0])
    return(latest)


def getLatestIngestionTimeMinusOne(s2w):
    thresh_date=datetime.now() - timedelta(days=30)
    pipeline = [
        { "$match" : {"properties.ingestion_time" : {"$lte" : thresh_date}}},
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]
    
    aggrLatest=list(s2w.aggregate(pipeline=pipeline))
    latest=list()
    
    for feat in aggrLatest:
        poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']})
        latest.append(poly[0])
    return(latest)


def getLatestPolysMinusOne(s2w):
    thresh_date=datetime.now() - timedelta(days=30)
    pipeline = [
        { "$match" : {"properties.ingestion_time" : {"$lte" : thresh_date}}},
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]
    
    aggrLatest=list(s2w.aggregate(pipeline=pipeline))
    
    latest=list()
    
    for feat in aggrLatest:
        poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']})
        latest.append(poly[0])
    return(latest)







def getTimeSeries(s2w):
    pipeline = [
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "timeSeries" : { "$push" : { "time" : "$properties.ingestion_time" , "area" : "$properties.area"} }
            }
            
        }
    ]

    TimeSeries = list(s2w.aggregate(pipeline=pipeline))
    return(TimeSeries)
