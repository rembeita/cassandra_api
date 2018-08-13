import boto3
import os
import socket
import tempfile
import shutil
from config_server import ConfigServer
from distutils.dir_util import copy_tree
from resources.nodetool import Nodetool
from resources.cqlsh import Cqlsh

class LocalRestore():
	def __init__(self):
		cfgins = ConfigServer()
		self.cfg = cfgins.getcfg()
		self.hostname = socket.gethostname()

	def getSnapshotTables(self, keyspace):
		path = self.cfg['local_backup']['path'] + '/' + self.hostname + '/' + keyspace
		print(path)
		tables = []


		for x in os.listdir(path):
			print(x)
			if os.path.isdir(os.path.join(os.path.abspath(path), x)): # check whether the current object is a folder or not
				tables.append(os.path.join(os.path.abspath(path), x))

		tables.sort()
		return tables


	def restoreTables(self, act_tables, snap_tables, keyspace):
		for act_table in act_tables:
			table_short_name = act_table.split('/')[-1].split("-")[0]
			print(table_short_name)
			for snap_table in snap_tables:
				snap_table_short_name = snap_table.split('/')[-2]
				if (table_short_name == snap_table_short_name):
					cqlsh = Cqlsh()
					cqlsh.drop_table(keyspace, table_short_name)
					cqlsh.create_table(act_table)
					copy_tree(snap_table, act_table)
					self.refreshTable(keyspace, table_short_name)
					st = os.stat(snap_table)
					for root, dirs, files in os.walk(act_table):
						for name in files:
							file_chown = os.path.join(root, name)
							os.chown(file_chown, st.st_uid, st.st_gid)
						for name in dirs:
							dirs_chown = os.path.join(root, name)
							os.chown(dirs_chown, st.st_uid, st.st_gid)
		return 'ok'


	def getLatestSnapshot(self, table_dir):
		snaps = []
		snaps_tables_final = []
		for snap_tables in table_dir:
			for x in os.listdir(snap_tables):
				if os.path.isdir(os.path.join(os.path.abspath(snap_tables), x)): # check whether the current object is a folder or not
					snaps.append(os.path.join(os.path.abspath(snap_tables), x))

			snaps.sort()
			snaps_tables_final.append(snaps[-1])
		return snaps_tables_final



	def getActiveTables(self, keyspace):
		keyspace_data_dir =  self.cfg['server']['cassandra_data'] + '/' + keyspace	
		tables = []
		for x in os.listdir(keyspace_data_dir):
			print(x)
			if os.path.isdir(os.path.join(os.path.abspath(keyspace_data_dir), x)): # check whether the current object is a folder or not
				tables.append(os.path.join(os.path.abspath(keyspace_data_dir), x))

		return tables
	

	def refreshTable(self, keyspace, table):
		nodetool = Nodetool()
		nodetool.do_refresh(keyspace, table)
	
	def getSnapshotTable(self, keyspace, table):
		tables = []
		tablepath = self.cfg['local_backup']['path'] + '/' + self.hostname + '/' + keyspace + '/' + table
		print(tablepath)
		tables.append(tablepath)
		return tables
	
	def getActiveTable(self, keyspace, table):
		keyspace_data_dir =  self.cfg['server']['cassandra_data'] + '/' + keyspace	
		tables = []
		for x in os.listdir(keyspace_data_dir):
			if os.path.isdir(os.path.join(os.path.abspath(keyspace_data_dir), x)): # check whether the current object is a folder or not
				if (str(x).find(table + "-") >= 0):
					print("encontre")
					print(x)
					tables.append(os.path.join(os.path.abspath(keyspace_data_dir), x))

		print(tables)
		return tables
	
	def getLatestSnapshot(self, table_dir):
		snaps = []
		snaps_tables_final = []
		for snap_tables in table_dir:
			for x in os.listdir(snap_tables):
				if os.path.isdir(os.path.join(os.path.abspath(snap_tables), x)): # check whether the current object is a folder or not
					snaps.append(os.path.join(os.path.abspath(snap_tables), x))

			snaps.sort()
			snaps_tables_final.append(snaps[-1])
		return snaps_tables_final
