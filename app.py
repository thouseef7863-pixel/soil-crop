"""
app.py - Main Flask Application
# Reloaded backend with real dataset model
Soil Crop Prediction System

Routes:
  GET  /              → Home Page
  GET  /predict       → Soil Input Form
  POST /predict       → Process Prediction → Result Page
  GET  /history       → Prediction History
  GET  /admin/crops   → Admin Dataset (list)
  POST /admin/crops   → Add Crop (AJAX/JSON)
  PUT  /admin/crops/<id> → Update Crop (AJAX/JSON)
  DELETE /admin/crops/<id> → Delete Crop (AJAX/JSON)
"""

import os 
import joblib 
import numpy as np 
from flask import Flask ,render_template ,request ,redirect ,url_for ,jsonify ,flash 
from models import db ,PredictionHistory ,CropDataset 
from datetime import datetime 




app =Flask (__name__ )
app .secret_key ='soil_crop_secret_key_2024'


app .config ['SQLALCHEMY_DATABASE_URI']=(
'sqlite:///'+os .path .join (os .path .abspath (os .path .dirname (__file__ )),'soil_crop_db.sqlite')
)
app .config ['SQLALCHEMY_TRACK_MODIFICATIONS']=False 


db .init_app (app )




MODEL_PATH =os .path .join ('models','crop_model.pkl')
SCALER_PATH =os .path .join ('models','scaler.pkl')

try :
    model =joblib .load (MODEL_PATH )
    scaler =joblib .load (SCALER_PATH )
    print ("✅ ML Model and Scaler loaded successfully.")
except FileNotFoundError :
    model =None 
    scaler =None 
    print ("⚠️  Model files not found. Run train_model.py first.")





VALID_RANGES ={
'nitrogen':(0 ,140 ,'Nitrogen (N)'),
'phosphorus':(5 ,145 ,'Phosphorus (P)'),
'potassium':(5 ,205 ,'Potassium (K)'),
'ph':(3.5 ,9.5 ,'pH'),
'temperature':(8 ,44 ,'Temperature (°C)'),
'humidity':(14 ,100 ,'Humidity (%)'),
'rainfall':(20 ,300 ,'Rainfall (mm)'),
}

def validate_inputs (form_data ):
    """
    Validates that all soil parameters are numeric and within allowed ranges.
    Returns (parsed_dict, error_message).
    On success error_message is None; on failure parsed_dict is None.
    """
    parsed ={}
    for field ,(lo ,hi ,label )in VALID_RANGES .items ():
        raw =form_data .get (field ,'').strip ()
        if not raw :
            return None ,f"{label } is required."
        try :
            val =float (raw )
        except ValueError :
            return None ,f"{label } must be a numeric value."
        if not (lo <=val <=hi ):
            return None ,f"{label } must be between {lo } and {hi }."
        parsed [field ]=val 
    return parsed ,None 







@app .route ('/')
def home ():
    """Renders the home/landing page with project introduction."""
    total_predictions =PredictionHistory .query .count ()
    total_crops =CropDataset .query .count ()
    recent =PredictionHistory .query .order_by (
    PredictionHistory .timestamp .desc ()).limit (3 ).all ()
    return render_template (
    'home.html',
    total_predictions =total_predictions ,
    total_crops =total_crops ,
    recent =recent 
    )



@app .route ('/predict',methods =['GET','POST'])
def predict ():
    """
    GET:  Renders the soil parameter input form.
    POST: Validates inputs, runs ML inference, saves to DB,
          and renders the result page.
    """
    if request .method =='GET':
        return render_template ('predict.html')


    if model is None or scaler is None :
        flash ('ML model is not loaded. Please run train_model.py first.','danger')
        return render_template ('predict.html')


    parsed ,error =validate_inputs (request .form )
    if error :
        flash (error ,'danger')
        return render_template ('predict.html',form_data =request .form )


    features =np .array ([[
    parsed ['nitrogen'],
    parsed ['phosphorus'],
    parsed ['potassium'],
    parsed ['ph'],
    parsed ['temperature'],
    parsed ['humidity'],
    parsed ['rainfall'],
    ]])


    features_scaled =scaler .transform (features )
    predicted_crop =model .predict (features_scaled )[0 ]
    probabilities =model .predict_proba (features_scaled )[0 ]
    confidence =float (np .max (probabilities ))*100 


    record =PredictionHistory (
    nitrogen =parsed ['nitrogen'],
    phosphorus =parsed ['phosphorus'],
    potassium =parsed ['potassium'],
    ph =parsed ['ph'],
    temperature =parsed ['temperature'],
    humidity =parsed ['humidity'],
    rainfall =parsed ['rainfall'],
    predicted_crop =predicted_crop ,
    confidence =confidence ,
    )
    db .session .add (record )
    db .session .commit ()

    return render_template (
    'result.html',
    crop =predicted_crop ,
    confidence =round (confidence ,2 ),
    inputs =parsed ,
    record_id =record .id ,
    timestamp =record .timestamp .strftime ('%Y-%m-%d %H:%M:%S')
    )



@app .route ('/history')
def history ():
    """Displays all past predictions in a sortable table."""
    page =request .args .get ('page',1 ,type =int )
    per_page =15 
    records =PredictionHistory .query .order_by (PredictionHistory .timestamp .desc ()).paginate (page =page ,per_page =per_page ,error_out =False )
    return render_template ('history.html',records =records )



@app .route ('/admin/crops',methods =['GET'])
def admin_crops ():
    """Renders admin page listing all crop dataset entries."""
    crops =CropDataset .query .order_by (CropDataset .crop_name ).all ()
    return render_template ('admin.html',crops =crops )


@app .route ('/admin/crops',methods =['POST'])
def add_crop ():
    """
    API: Add a new crop to the dataset.
    Expects JSON body with crop fields.
    Returns JSON response.
    """
    data =request .get_json ()
    if not data :
        return jsonify ({'success':False ,'message':'No data provided'}),400 

    required =['crop_name','nitrogen','phosphorus','potassium',
    'ph','temperature','humidity','rainfall']
    for field in required :
        if field not in data or data [field ]=='':
            return jsonify ({'success':False ,'message':f'{field } is required'}),400 

    try :
        crop =CropDataset (
        crop_name =str (data ['crop_name']).strip (),
        nitrogen =float (data ['nitrogen']),
        phosphorus =float (data ['phosphorus']),
        potassium =float (data ['potassium']),
        ph =float (data ['ph']),
        temperature =float (data ['temperature']),
        humidity =float (data ['humidity']),
        rainfall =float (data ['rainfall']),
        season =str (data .get ('season','')).strip (),
        description =str (data .get ('description','')).strip (),
        )
        db .session .add (crop )
        db .session .commit ()
        return jsonify ({'success':True ,'message':'Crop added successfully!',
        'crop':crop .to_dict ()}),201 
    except Exception as e :
        db .session .rollback ()
        return jsonify ({'success':False ,'message':str (e )}),500 


@app .route ('/admin/crops/<int:crop_id>',methods =['PUT'])
def update_crop (crop_id ):
    """
    API: Update an existing crop record by ID.
    Expects JSON body with updated fields.
    Returns JSON response.
    """
    crop =CropDataset .query .get_or_404 (crop_id )
    data =request .get_json ()
    if not data :
        return jsonify ({'success':False ,'message':'No data provided'}),400 

    try :
        crop .crop_name =str (data .get ('crop_name',crop .crop_name )).strip ()
        crop .nitrogen =float (data .get ('nitrogen',crop .nitrogen ))
        crop .phosphorus =float (data .get ('phosphorus',crop .phosphorus ))
        crop .potassium =float (data .get ('potassium',crop .potassium ))
        crop .ph =float (data .get ('ph',crop .ph ))
        crop .temperature =float (data .get ('temperature',crop .temperature ))
        crop .humidity =float (data .get ('humidity',crop .humidity ))
        crop .rainfall =float (data .get ('rainfall',crop .rainfall ))
        crop .season =str (data .get ('season',crop .season or '')).strip ()
        crop .description =str (data .get ('description',crop .description or '')).strip ()
        crop .updated_at =datetime .utcnow ()
        db .session .commit ()
        return jsonify ({'success':True ,'message':'Crop updated successfully!',
        'crop':crop .to_dict ()})
    except Exception as e :
        db .session .rollback ()
        return jsonify ({'success':False ,'message':str (e )}),500 


@app .route ('/admin/crops/<int:crop_id>',methods =['DELETE'])
def delete_crop (crop_id ):
    """
    API: Delete a crop record by ID.
    Returns JSON response.
    """
    crop =CropDataset .query .get_or_404 (crop_id )
    try :
        db .session .delete (crop )
        db .session .commit ()
        return jsonify ({'success':True ,'message':'Crop deleted successfully!'})
    except Exception as e :
        db .session .rollback ()
        return jsonify ({'success':False ,'message':str (e )}),500 





if __name__ =='__main__':
    with app .app_context ():
        db .create_all ()
        print ("✅ Database tables created/verified.")
    app .run (debug =True ,host ='0.0.0.0',port =5000 )
