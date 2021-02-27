from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from telebot import TeleBot

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

telegram_bot = TeleBot(app.config['BOT_TOKEN'])

from app import routes, models, messages, telegram_bot