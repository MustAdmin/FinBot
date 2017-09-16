# -*- coding: utf-8 -*-

"""
Script for creating MongoDB connection


@author: Koushik Khan [write2koushik.stat@outlook.com]
@copyright: MUST Research Club [www.must.co.in]
"""

import os
import sys
import json
from configparser import RawConfigParser
import pymongo as pm
import pandas as pd
from datetime import datetime
from bson.objectid import ObjectId

class DatabaseUtilities(object):
    """
    For database connection
    """
    def __init__(self, host, port, usr, pswd, db):
        self.host = host
        self.port = port
        self.usr = usr
        self.pswd = pswd
        self.db = db

    def connect_to_db(self):
        """
        Establishes connection to the database
        return: a db object, can be used to access and collections
        """
        if self.usr and self.pswd:
            # print(self.usr, self.pswd, self.host, self.port)
            mongo_url = "mongodb://%s:%s@%s:%s" % (self.usr, self.pswd, self.host, self.port)
        else:
            mongo_url = "mongodb://%s:%s" % (self.host, self.port)
        try:
            conn = pm.MongoClient(mongo_url)
            db = conn[self.db]
            return db
        except:
            return -990 # "Status":"Error connecting to the database

    def download_data(self, collection_name, db, make_lower=False):
        """
        Converts MongoDB collections into Pandas DataFrame.
        make_lower=True converts the whole DataFrame in lower case.
        """
        if make_lower:
            #try:
            #    df = pd.DataFrame(list(db[collection_name].find({"processed": {"$ne":"Y"}}))).apply(lambda x: x.astype(str).str.lower())
            #except:
            #    df = pd.DataFrame(list(db[collection_name].find())).apply(lambda x: x.astype(str).str.lower())
            df = pd.DataFrame(list(db[collection_name].find())).apply(lambda x: x.astype(str).str.lower())
        else:
            #try:
            #    df = pd.DataFrame(list(db[collection_name].find({"processed": {"$ne":"Y"}})))
            #except:
            #    df = pd.DataFrame(list(db[collection_name].find()))
            df = pd.DataFrame(list(db[collection_name].find()))
        return df

    def write_data(self, collection_name, df, db):
        """
        'collection_name': string containing the name of the collection
        'df': dataframe containing the records to be written to the collection
        """
        try:
            result = db[collection_name].insert_many(df.to_dict('records'))
            print('# -------------------------- #')
            print('Inserted document ids: ', result.inserted_ids)
            return 0
        except Exception:
            return -991 # "Status":"Error uploading pre-processed data"


if __name__=="__main__":
    # create connection object
    con_obj = DatabaseUtilities('xxx.xxx.xxx.xxx', 'xxxx', 'xxxxxxxx', 'xxxxxxxxxxxxxxxxxxxx', 'xxxxxxx')
    db = con_obj.connect_to_db()

    data = pd.read_csv(r"path/to/csv")

    con_obj.write_data("DummyDefectCollection", data, db)
