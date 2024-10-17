import os

class Config:
    DEBUG = True
    DATABASE_URI = os.getenv('DATABASE_URI', 'mongodb://localhost:27017/rule_engine')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

config = Config()
