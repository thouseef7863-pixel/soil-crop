"""
config.py - Configuration classes for the Flask application
"""

import os 

basedir =os .path .abspath (os .path .dirname (__file__ ))


class Config :
    """Base configuration."""
    SECRET_KEY =os .environ .get ('SECRET_KEY')or 'soil_crop_secret_key_2024'
    SQLALCHEMY_TRACK_MODIFICATIONS =False 


    MODEL_PATH =os .path .join (basedir ,'models','crop_model.pkl')
    SCALER_PATH =os .path .join (basedir ,'models','scaler.pkl')


class DevelopmentConfig (Config ):
    """Development configuration — local MySQL."""
    DEBUG =True 
    SQLALCHEMY_DATABASE_URI =os .environ .get ('DATABASE_URL')or 'sqlite:///'+os .path .join (basedir ,'soil_crop_db.sqlite')


class ProductionConfig (Config ):
    """Production configuration."""
    DEBUG =False 
    SQLALCHEMY_DATABASE_URI =os .environ .get ('DATABASE_URL')or 'sqlite:///'+os .path .join (basedir ,'soil_crop_db.sqlite')


config ={
'development':DevelopmentConfig ,
'production':ProductionConfig ,
'default':DevelopmentConfig ,
}
