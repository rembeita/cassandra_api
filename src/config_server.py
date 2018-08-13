import yaml

class ConfigServer():
	def getcfg(self):
		with open("config.yaml", 'r') as ymlfile:
			return yaml.load(ymlfile)

