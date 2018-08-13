import os
import socket
import shutil
from config_server import ConfigServer
from distutils.dir_util import copy_tree

class LocalBackup():
	def deleteSnapshot(self, snapdir):
		print("deleting snapshot dir " + snapdir)
		shutil.rmtree(snapdir)

	def uploadDirectory(self, from_directory, toDir, snapshot_num, keyspace, table):
		hostname = socket.gethostname()
		table = table.split('-')[0]
		to_directory = toDir + '/' + hostname + '/' + keyspace + '/' + table 
		to_directory_snap = to_directory +'/' + snapshot_num
		if not os.path.exists(to_directory):
			os.makedirs(to_directory)
		shutil.copytree(from_directory, to_directory_snap)
		st = os.stat(from_directory)

		for root, dirs, files in os.walk(to_directory_snap):
			for name in files:
				file_chown = os.path.join(root, name)
				os.chown(file_chown, st.st_uid, st.st_gid)
			for name in dirs:
				dirs_chown = os.path.join(root, name)
				os.chown(dirs_chown, st.st_uid, st.st_gid)
		os.chown(to_directory_snap, st.st_uid, st.st_gid)
		self.deleteSnapshot(from_directory)



