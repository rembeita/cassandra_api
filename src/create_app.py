from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config_server import ConfigServer

db = SQLAlchemy()

def create_app():
	cfgins = ConfigServer()
	cfg = cfgins.getcfg()
	app = Flask(__name__)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = cfg['server']['sqlite_url']
	app.secret_key = "PageFreezer"
	db.init_app(app)
	return app


