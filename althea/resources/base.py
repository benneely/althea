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
#import sys
#sys.path.insert(0, os.path.expanduser('~/Dropbox/40-githubRrepos/althea/althea'))
from althea.dynamicloader import dynamicloader as dl
from althea import __app__, __filename__


module_path = os.path.dirname(__file__) 
#for qc: module_path = '/Users/nn31/Dropbox/40-githubRrepos/althea/althea'

def inputTableTuple(inputs,model_uuid):
    input_table = []
    choice_table = []
    for key,value in inputs.items():
        inputs_uuid = str(uuid.uuid4())
        _type = value.get('type')
        _name = key
        _question = value.get('question')
        input_table.append((inputs_uuid,model_uuid,_type,_name,_question))
        for x in value.get('responses'):
            choice_uuid = str(uuid.uuid4())
            choice_table.append((choice_uuid,inputs_uuid,x))
    return input_table, choice_table

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
               
class Metadata():
    def __init__(self, *args, **kwargs):
        self.database = os.path.join(appdirs.user_data_dir(__app__),__filename__)
        if not os.path.exists(os.path.dirname(self.database)):
            os.mkdir(os.path.dirname(self.database))
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute('''CREATE TABLE if not exists models
             (model_uuid text primary key, 
             name text, 
             doi text,
             response text,
             implementation_file text)''')
        c.execute('''CREATE TABLE if not exists inputs
             (input_uuid text primary key,
             model_uuid text,
             type text, 
             variable_name text, 
             elicit_question text)''')
        c.execute('''CREATE TABLE if not exists choices
             (choice_uuid text primary key,
             input_uuid text,
             display_text text)''')
             
        conn.commit()
        c.close()
        examples = kwargs.pop('add_examples')
        if examples:
            conn.row_factory = lambda cursor, row: row[0]
            c = conn.cursor()
            c.execute('SELECT doi FROM models')
            doi_indatabase = c.fetchall()
            c.close()
            conn.close()
            #print(doi_indatabase)
            if ('0.1161/CIRCULATIONAHA.108.816694' not in doi_indatabase):
                print('doi not found')
                self.add(function_location=os.path.join(module_path, 'model_db','framingham30yr','score.py'),
                         inputs={'male':{'type':'categorical','question':'Gender ?','responses':['Yes','No']},
                         'age':{'type':'continuous','question':'Age (years)','responses':[25]},
                         'sbp':{'type':'continuous','question':'Systolic Blood Pressure (mmHg)','responses':[110]},                         
                         'tc':{'type':'continuous','question':'Total Cholesterol (mg/dl)','responses':[150]},
                         'hdlc':{'type':'continuous','question':'HDL Cholesterol (mg/dl)','responses':[60]},
                         'trtbp':{'type':'categorical','question':'Antihypertensive Treatment?','responses':['Yes','No']},
                         'smoke':{'type':'categorical','question':'Self-reported cigarette smoking in the year preceding the examination','responses':['Yes','No']},
                         'diab':{'type':'categorical','questions':'Fasting glucose >= 126 mg/dl or use of insulin or oral hypoglycemic medications','responses':['Yes','No']}},
                         name='Framingham 30 Year CVD Risk (Lipids)',
                         response='CVD',
                         doi='0.1161/CIRCULATIONAHA.108.816694')
                self.add(function_location=os.path.join(module_path, 'model_db','pooledCohorts','score.py'),
                         inputs={'male':{'type':'categorical','question':'Gender ?','responses':['Yes','No']},
                         'nonHispAA':{'type':'categorical','question':'Ethnicity: non-hispanic african american?','responses':['Yes','No']},
                         'age':{'type':'continuous','question':'Age (years)','responses':[25]},
                         'sbp':{'type':'continuous','question':'Systolic Blood Pressure (mmHg)','responses':[110]},
                         'trtbp':{'type':'categorical','question':'Antihypertensive Treatment?','responses':['Yes','No']},
                         'tc':{'type':'continuous','question':'Total Cholesterol (mg/dl)','responses':[150]},
                         'hdlc':{'type':'continuous','question':'HDL Cholesterol (mg/dl)','responses':[60]},
                         'diab':{'type':'categorical','questions':'Fasting glucose >= 126 mg/dl or use of insulin or oral hypoglycemic medications','responses':['Yes','No']},
                         'smoke':{'type':'categorical','question':'Self-reported cigarette smoking in the year preceding the examination','responses':['Yes','No']}},
                         name='2013 ACC/AHA Pooled Cohorts Equation CVD',
                         response='ASCVD',
                         doi='10.1161/01.cir.0000437741.48606.98')
        #for debug: SELECT name, sql FROM sqlite_master WHERE type='table';
    def add(self, *args, **kwargs):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        model_uuid = str(uuid.uuid4())
        function_location = kwargs.pop('function_location')
        name = kwargs.pop('name')
        response = kwargs.pop('response')
        doi = kwargs.pop('doi')
        inputs = kwargs.pop('inputs')
        c.execute("INSERT INTO models (model_uuid,name,doi,response,implementation_file) VALUES (?,?,?,?,?)",
                  (model_uuid,name,doi,response,function_location))
        input_table, choice_table = inputTableTuple(inputs,model_uuid)
        c.executemany("INSERT INTO inputs (input_uuid,model_uuid,type,variable_name,elicit_question) VALUES (?,?,?,?,?)",
                  input_table)
        c.executemany("INSERT INTO choices (choice_uuid,input_uuid,display_text) VALUES (?,?,?)",
                  choice_table)
        conn.commit()
        c.close()
        conn.close()
    def available_models(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("select model_uuid,name from models")
        return c.fetchall()
        c.close()
        conn.close()

class Model(): 
    def __init__(self,model_uuid):
        self.database = os.path.join(appdirs.user_data_dir(__app__),__filename__)
        self.model_uuid = model_uuid
        conn = sqlite3.connect(self.database)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql = "select input_uuid, type, variable_name, elicit_question from inputs where model_uuid=?"
        c.execute(sql,[(self.model_uuid)])
        metadata = c.fetchall()
        if len(metadata)==0:
            raise ValueError('The model_uuid provided is not in the database.')    
        sql = "select name,response, doi, implementation_file from models where model_uuid=?"
        c.execute(sql,[(self.model_uuid)])
        model = c.fetchall()
        self.model_name = model[0].get('name')     
        self.doi = model[0].get('doi')
        self.score_file = model[0].get('implementation_file')
        self.response = model[0].get('response')
        def __model_input_choices(input_uuid):
            sql = "select display_text from choices where input_uuid=?"
            c.execute(sql,[(input_uuid)])
            results = c.fetchall()
            return [x.get('display_text') for x in results]
        self.ask = {x.get('elicit_question'): __model_input_choices(x.get('input_uuid')) for x in metadata}
        self.parameter_name = [x.get('variable_name') for x in metadata]
        self.variable_type = [x.get('type') for x in metadata]
        c.close()
        conn.close()
    def score(self,**kwargs):
        #first we need to make sure that the inputs match the metadata
        vars_in_model_not_in_call = set(self.parameter_name).difference(set(kwargs.keys()))
        if not len(vars_in_model_not_in_call)==0:
            raise ValueError("Trying to use method score, but named input parameters don't match intended function.")   
        real_score_fnc = dl.dynamic_score(self.score_file)
        result = real_score_fnc(kwargs)
        return(result)
