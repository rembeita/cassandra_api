from flask_restful import Resource, reqparse
from resources.nodetool import Nodetool
from resources.s3backup import S3Backup
from resources.localbackup import LocalBackup
from config_server import ConfigServer
from models.backups import BackupModel
import os
import threading
from db import db
from flask import Flask
from create_app import create_app


class Cas_Snapshot(Resource):
#       @jwt_required()
	def __init__(self):
		cfgins = ConfigServer()
		self.cfg = cfgins.getcfg()

	def get(self, name):
		return {'pagefreezer': name}

	def post(self, keyspace=''):
		keyspacev = keyspace

		t = threading.Thread(target=self.create_backup, args=(keyspace,))
		threads = []
		threads.append(t)
		t.start()

		#_thread.start_new_thread(self.create_backup, (keyspace,))
		return {'result': 'ok'}

	def create_backup(self, keyspace):
		app = create_app()
		app.app_context().push()

		nodetool = Nodetool()
		output, error = nodetool.do_snapshot(keyspace)
		snapshot_num = str(output).split("Snapshot directory:")[1].replace(' ','').replace("'",'').replace("\\n",'')
		directory_cass = self.cfg['server']['cassandra_data'] + '/' + keyspace + '/'
		keyspacedir = os.listdir(directory_cass)
		backup = BackupModel(snapshot_num, 'running', False, 'undefined', keyspace) 
		backup.save_to_db()
		for table in keyspacedir:
			directory_cass_snap = directory_cass + table + '/snapshots/' + snapshot_num
			if (self.cfg['s3']['s3_enabled']):
				s3 = S3Backup()
				s3.uploadDirectory(directory_cass_snap, keyspace, snapshot_num, table)
				backup.location = 's3'
				backup.state = 'Finish'
				backup.completed = True

			if (self.cfg['local_backup']['lb_enabled']):
				local_backup = LocalBackup()
				local_backup.uploadDirectory(directory_cass_snap, self.cfg['local_backup']['path'], snapshot_num , keyspace, table)
				backup.location = self.cfg['local_backup']['path']
				backup.state = 'Finish'
				backup.completed = True

		backup.save_to_db()


 

