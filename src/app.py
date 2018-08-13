import yaml
import argparse

from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from resources.cassandra import Cas_Base
from resources.cassandra_snapshot import Cas_Snapshot
from resources.cassandra_restore import Cas_Restore
from resources.cassandra_restore_table import Cas_Restore_Table
from config_server import ConfigServer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists

#from db import db
#with open("config.yaml", 'r') as ymlfile:
#	cfg = yaml.load(ymlfile)
from create_app import create_app

token_lease_time = '5m'
token_num_uses = '5'


cfgins = ConfigServer()
cfg = cfgins.getcfg()

app = create_app()
api = Api(app)
jwt = JWT(app, authenticate, identity) # /auth


api.add_resource(Cas_Base,'/cassandra/') 
api.add_resource(Cas_Snapshot,'/cassandra/snapshot/<string:keyspace>') 
api.add_resource(Cas_Restore,'/cassandra/restore/<string:keyspace>') 
api.add_resource(Cas_Restore_Table,'/cassandra/restore/<string:keyspace>/<string:table>/') 

if __name__ == '__main__':
#	db.init_app(app)
	app.run(host=cfg['server']['bind'],port=int(cfg['server']['port']), debug=True)
