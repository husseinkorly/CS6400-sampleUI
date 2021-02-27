from flask import Flask
from .database import Database
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
Database.init(Config)

from app import routes
