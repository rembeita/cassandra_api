import subprocess

class Cqlsh():
	def __init__(self):
		print("Creating cqlsh instance")

	def drop_table(self, keyspace, table):
		print("Removing table " + table + " of keyspace " + keyspace)
		bashCommand_drop = "cqlsh -e \" drop table " + keyspace + "." + table + "\""
		print(bashCommand_drop)

		process_drop = subprocess.Popen(bashCommand_drop.split(), stdout=subprocess.PIPE)
		output_drop, error_drop = process_drop.communicate()
		print("ESTO ES DROP")
		print(output_drop)
		print(error_drop)
		print("TERMINE DROP")
		return output_drop, error_drop

	def create_table(self, table_dir):
		print("create table " + table_dir )
		bashCommand_create = "cqlsh -f " +   table_dir + "/schema.cql"
		print(bashCommand_create)

		process_create = subprocess.Popen(bashCommand_create.split(), stdout=subprocess.PIPE)
		output_create, error_create = process_create.communicate()
		print("ESTO ES CREATE")
		print(output_create)
		print(error_create)
		print("TERMINE CREATE")
		return output_create, error_create
