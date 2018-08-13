import boto3
import os
from config_server import ConfigServer
import socket

class S3Backup():
	def __init__(self):
		cfgins = ConfigServer()
		cfg = cfgins.getcfg()
		self.access_key = cfg['s3']['access_key']
		self.secret_key = cfg['s3']['secret_key']
		self.bucket_name = cfg['s3']['bucket_name']
		self.client = boto3.client(
		    's3',
		    aws_access_key_id = self.access_key,
		    aws_secret_access_key = self.secret_key,
		)

	def uploadDirectory(self, path, keyspace, snapshot_num, table):
		print(path)
		table = table.split('-')
		hostname = socket.gethostname()
		key = hostname + '/' + keyspace + '/' + table + '/' + snapshot_num + '/'
		for root,dirs,files in os.walk(path):
			print(root)
			for file in files:
				self.client.upload_file(os.path.join(root,file), self.bucket_name, key + file)
		print("termine")


#		for filename in os.listdir(path):
#			logger.warn('Uploading %s to Amazon S3 bucket %s' % (filename, self.bucket_name))
#			s3.Object(self.bucket_name, filename).put(Body=open(os.path.join(path, filename), 'rb'))
#		        logger.info('File uploaded to https://s3.%s.amazonaws.com/%s/%s' % (self.bucket_name, filename))
