"""
train_model.py - ML Model Training Script
Trains a RandomForestClassifier on the Crop Recommendation dataset
and saves the model + scaler as .pkl files using joblib.

Run this script ONCE before starting the Flask application:
    python train_model.py
"""

import os 
import numpy as np 
import pandas as pd 
from sklearn .ensemble import RandomForestClassifier 
from sklearn .preprocessing import StandardScaler 
from sklearn .model_selection import train_test_split 
from sklearn .metrics import accuracy_score 
import joblib 




dataset_path =os .path .join ('dataset','Crop_recommendation.csv')
print (f"📥 Loading dataset from {dataset_path }...")
df =pd .read_csv (dataset_path )


df =df .dropna ()

print (f"✅ Loaded {len (df )} real training samples for {df ['label'].nunique ()} crops")
print (f"   Crops: {sorted (df ['label'].unique ())}\n")






X =df [['N','P','K','ph','temperature','humidity','rainfall']]
y =df ['label']

X_train ,X_test ,y_train ,y_test =train_test_split (
X ,y ,test_size =0.2 ,random_state =42 ,stratify =y 
)




scaler =StandardScaler ()
X_train_scaled =scaler .fit_transform (X_train )
X_test_scaled =scaler .transform (X_test )




model =RandomForestClassifier (
n_estimators =200 ,
max_depth =None ,
random_state =42 ,
n_jobs =-1 
)
model .fit (X_train_scaled ,y_train )


y_pred =model .predict (X_test_scaled )
acc =accuracy_score (y_test ,y_pred )
print (f"📊 Model Accuracy on Test Set: {acc *100 :.2f}%\n")




os .makedirs ('models',exist_ok =True )
joblib .dump (model ,'models/crop_model.pkl')
joblib .dump (scaler ,'models/scaler.pkl')

print ("💾 Saved: models/crop_model.pkl")
print ("💾 Saved: models/scaler.pkl")
print ("\n🚀 You can now start the Flask app with: python app.py")
