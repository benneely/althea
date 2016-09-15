# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 15:01:17 2016

@author: nn31
"""
import appdirs
import os
import pickle
import socket
import datetime
import uuid
import sqlite3

__app__='althea'
__filename__='althea.db'


class DataModel():
    def __init__(self, *args, **kwargs):
        self.database = os.path.join(appdirs.user_data_dir(__app__),__filename__)
        if not os.path.exists(self.database):
            os.mkdir(os.path.dirname(self.database))
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute('''CREATE TABLE if not exists model
             (model_uuid text primary key, 
             name text, 
             doi text,
             response text,
             implementation_file text)''')
        c.execute('''CREATE TABLE if not exists inputs
             (inputs_uuid text primary key,
             model_uuid text,
             type text, 
             variable_name text, 
             elicit_question text)''')
        c.execute('''CREATE TABLE if not exists choices
             (choice_uuid text primary key,
             input_uuid text,ß
             display_text text, 
             weight real, 
             elicit_question text)''')
             
        conn.commit()
        c.close()
        conn.close()
        #for debug: SELECT name, sql FROM sqlite_master WHERE type='table';
    def add(self, *args, **kwargs):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        model_uuid = str(uuid.uuid4())
        input_uuid = str(uuid.uuid4())
        choice_uuid = str(uuid.uuid4())
        function_location = kwargs.pop('function_location')
        name = kwargs.pop('name')
        response = kwargs.pop('response')
        doi = kwargs.pop('doi')
        c.execute("INSERT INTO model (model_uuid,name,doi,response,implementation_file) VALUES (?,?,?,?,?)",
                  (model_uuid,name,doi,response,function_location));
        conn.commit()
        c.close()
        conn.close()

class AltheaData():
    def __init__(self, *args, **kwargs):
        self.database = os.path.join(appdirs.user_data_dir(__app__),__filename__)
        if os.path.exists(self.database):
            with open(self.database,'rb') as f:
                self.datamodel = pickle.load(f)
        else:
            self.datamodel={}
            self.datamodel['machine'] = socket.gethostname()
            self.datamodel['models'] = {}            
    def save_changes(self):
        self.datamodel['last_update'] = datetime.datetime.now().strftime('%Y_%m_%d_%H.%M')
        if not os.path.exists(self.database):
            os.mkdir(os.path.dirname(self.database))
        with open(self.database, 'wb') as f:
            pickle.dump(self.datamodel, f)
    def add(self, *args, **kwargs):
        temp_id = str(uuid.uuid4())
        self.datamodel['models'][temp_id] = {}
        self.datamodel['models'][temp_id]['location'] = kwargs.pop('location')
        self.datamodel['models'][temp_id]['filename'] = kwargs.pop('filename')
        self.datamodel['models'][temp_id]['short_name'] = kwargs.pop('short_name')
        self.datamodel['models'][temp_id]['doi'] = kwargs.pop('doi')
        self.datamodel['models'][temp_id]['response'] = kwargs.pop('response')
        self.datamodel['models'][temp_id]['inputs']   = kwargs.pop('inputs')
        
        
       
if not os.path.exists(database):
            os.mkdir(os.path.dirname(database))  

a = AltheaData()
a.add(function_location='/Users/nn31/Dropbox/40-githubRrepos/althea/althea/model_db/pooledCohorts/score.py',
      inputs=['male','nonHispAA','age','sbp','trtbp','tcl','hdl','diab','smoke'],
      name='2013 ACC/AHA Pooled Cohorts Equation CVD',
      response='ASCVD',
      doi='10.1161/01.cir.0000437741.48606.98/-/DC1')   
a.save_changes()       


