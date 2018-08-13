from flask_restful import Resource, reqparse
from resources.nodetool import Nodetool

class Cas_Base(Resource):
#       @jwt_required()
	def get(self):
		return {'pagefreezer': 'get'}

	def post(self):
		return {'pagefreezer': 'post'}
