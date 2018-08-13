from flask_restful import Resource, reqparse
from resources.nodetool import Nodetool
from resources.s3backup import S3Backup
from resources.localrestore import LocalRestore
from config_server import ConfigServer
import os
from db import db
from flask import Flask
from create_app import create_app
import threading



class Cas_Restore_Table(Resource):
#       @jwt_required()
	def __init__(self):
		cfgins = ConfigServer()
		self.cfg = cfgins.getcfg()

	def get(self, keyspace):
		return {'pagefreezer': 'Recover API ' + name}

	def post(self, keyspace, table):
		t = threading.Thread(target=self.restore_table_db, args=(keyspace, table))
		threads = []
		threads.append(t)
		t.start()
		return {'result': 'ok'}

	def restore_table_db(self, keyspace, table):
		lc = LocalRestore()
		snap_tables = lc.getSnapshotTable(keyspace, table)
		act_tables = lc.getActiveTable(keyspace, table)
		last_snaps = lc.getLatestSnapshot(snap_tables)
		nada = lc.restoreTables(act_tables, last_snaps, keyspace)
