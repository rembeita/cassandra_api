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



class Cas_Restore(Resource):
#       @jwt_required()
	def __init__(self):
		cfgins = ConfigServer()
		self.cfg = cfgins.getcfg()

	def get(self, keyspace):
		return {'pagefreezer': 'Recover API ' + name}

	def post(self, keyspace=''):
		keyspacev = keyspace
		print("ejecutando thread restore_db")
		t = threading.Thread(target=self.restore_db, args=(keyspace,))
		threads = []
		threads.append(t)
		t.start()
		#t.join()
		#self.restore_db(keyspacev)
		return {'result': 'ok'}

	def restore_db(self, keyspace):
		#app = create_app()
		#app.app_context().push()

		print("ejecutando thread lc")
		lc = LocalRestore()
		print("ejecutando thread getSnap")
		snap_tables = lc.getSnapshotTables(keyspace)
		print("ejecutando thread act_tables")
		act_tables = lc.getActiveTables(keyspace)
		print("ejecutando thread last_snaps")
		last_snaps = lc.getLatestSnapshot(snap_tables)
		print("ejecutando thread nada")
		nada = lc.restoreTables(act_tables, last_snaps, keyspace)
		#print(snap_tables)
		#print(act_tables)
		#print(last_snaps)
