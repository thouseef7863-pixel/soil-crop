"""
models.py - SQLAlchemy Database Models
Defines the database tables for the Soil Crop Prediction System
"""

from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 


db =SQLAlchemy ()


class PredictionHistory (db .Model ):
    """
    Stores each prediction made by the user including:
    - Soil input parameters
    - Predicted crop name
    - Model confidence score
    - Timestamp of prediction
    """
    __tablename__ ='prediction_history'

    id =db .Column (db .Integer ,primary_key =True ,autoincrement =True )
    nitrogen =db .Column (db .Float ,nullable =False )
    phosphorus =db .Column (db .Float ,nullable =False )
    potassium =db .Column (db .Float ,nullable =False )
    ph =db .Column (db .Float ,nullable =False )
    temperature =db .Column (db .Float ,nullable =False )
    humidity =db .Column (db .Float ,nullable =False )
    rainfall =db .Column (db .Float ,nullable =False )
    predicted_crop =db .Column (db .String (100 ),nullable =False )
    confidence =db .Column (db .Float ,nullable =False )
    timestamp =db .Column (db .DateTime ,default =datetime .utcnow )

    def to_dict (self ):
        """Convert model instance to dictionary for JSON responses."""
        return {
        'id':self .id ,
        'nitrogen':self .nitrogen ,
        'phosphorus':self .phosphorus ,
        'potassium':self .potassium ,
        'ph':self .ph ,
        'temperature':self .temperature ,
        'humidity':self .humidity ,
        'rainfall':self .rainfall ,
        'predicted_crop':self .predicted_crop ,
        'confidence':round (self .confidence ,2 ),
        'timestamp':self .timestamp .strftime ('%Y-%m-%d %H:%M:%S')
        }

    def __repr__ (self ):
        return f'<PredictionHistory id={self .id } crop={self .predicted_crop }>'


class CropDataset (db .Model ):
    """
    Admin-managed dataset of crop records.
    Used for CRUD operations in the Admin Dataset Management page.
    """
    __tablename__ ='crop_dataset'

    id =db .Column (db .Integer ,primary_key =True ,autoincrement =True )
    crop_name =db .Column (db .String (100 ),nullable =False )
    nitrogen =db .Column (db .Float ,nullable =False )
    phosphorus =db .Column (db .Float ,nullable =False )
    potassium =db .Column (db .Float ,nullable =False )
    ph =db .Column (db .Float ,nullable =False )
    temperature =db .Column (db .Float ,nullable =False )
    humidity =db .Column (db .Float ,nullable =False )
    rainfall =db .Column (db .Float ,nullable =False )
    season =db .Column (db .String (50 ),nullable =True )
    description =db .Column (db .Text ,nullable =True )
    created_at =db .Column (db .DateTime ,default =datetime .utcnow )
    updated_at =db .Column (db .DateTime ,default =datetime .utcnow ,onupdate =datetime .utcnow )

    def to_dict (self ):
        """Convert model instance to dictionary for JSON responses."""
        return {
        'id':self .id ,
        'crop_name':self .crop_name ,
        'nitrogen':self .nitrogen ,
        'phosphorus':self .phosphorus ,
        'potassium':self .potassium ,
        'ph':self .ph ,
        'temperature':self .temperature ,
        'humidity':self .humidity ,
        'rainfall':self .rainfall ,
        'season':self .season or '',
        'description':self .description or '',
        'created_at':self .created_at .strftime ('%Y-%m-%d %H:%M:%S'),
        'updated_at':self .updated_at .strftime ('%Y-%m-%d %H:%M:%S')if self .updated_at else ''
        }

    def __repr__ (self ):
        return f'<CropDataset id={self .id } crop={self .crop_name }>'
