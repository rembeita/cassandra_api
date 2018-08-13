import sqlite3
from flask_sqlalchemy import SQLAlchemy
import datetime
from db import db

class BackupModel(db.Model):
	__tablename__ = 'backups'
	id = db.Column(db.Integer, primary_key=True)
	snapshot = db.Column(db.String(255))
	state = db.Column(db.String(255))
	created_at = db.Column(db.DateTime, default=datetime.datetime.now())
	completed = db.Column(db.Boolean, unique=False, default=False)
	location = db.Column(db.String(20000))
	keyspaces = db.Column(db.String(20000))
	

	def __init__(self, snapshot, state,  completed, location, keyspaces):
		self.snapshot = snapshot
		self.state = state
		self.completed = completed
		self.location = location
		self.keyspaces = keyspaces

	@classmethod
	def find_by_id(cls, snapshot):
		return cls.query.filter_by(snapshot=snapshot).first()


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()


	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()




