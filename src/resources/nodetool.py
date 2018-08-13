import subprocess

class Nodetool():
	def __init__(self):
		print("Creating nodetool instance")

	def do_snapshot(self, name='All'):
		print("Creando backup " + name)
		if (name == 'All'):
			bashCommand = "nodetool snapshot"
		else:
			bashCommand = "nodetool snapshot " + name

		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()
		print(output)
		print(error)
		return output, error

	def do_refresh(self, keyspace, table):
		print("Refreshing table " + table + " of keyspace " + keyspace)
		bashCommand = "nodetool refresh " + keyspace + " " + table

		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()
		print(output)
		print(error)
		return output, error

