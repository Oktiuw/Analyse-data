# app/config.py
import os

basedir = os.path.abspath(os.path.dirname( __file__ ))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'un mot de passe à garder secret'

     # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://distant:azerty02@10.31.5.227/vinc0064_data'
   
    SQLALCHEMY_TRACK_MODIFICATIONS = False