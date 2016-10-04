# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from json import dumps
from althea import __app__, __filename__
from althea.resources.base import dict_factory, Model
import appdirs
import os
import sys


app = Flask(__name__)
database = os.path.join(appdirs.user_data_dir(__app__),__filename__)


app = Flask(__name__)
api = Api(app)

class Althea_Meta(Resource):
    def get(self):
        #Connect to databse
        conn = sqlite3.connect(database)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql = "select * from models"
        c.execute(sql)
        metadata = c.fetchall()
        return metadata

class Model_Input(Resource):
    def get(self, model_uuid):
        conn = sqlite3.connect(database)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql = "select * from inputs where model_uuid=?"
        c.execute(sql,[(model_uuid)])
        metadata = c.fetchall()
        return metadata
        

api.add_resource(Model_Input, '/models/<string:model_uuid>/inputs')
api.add_resource(Althea_Meta, '/models')

    
def main():
    try:
        port = int(sys.argv[1])
    except:
        port = 8002
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()