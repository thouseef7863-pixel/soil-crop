"""
main.py — Entry point for running the Soil Crop Prediction System

Quick Start:
    1. Install dependencies:
        pip install -r requirements.txt

    2. Create MySQL database (run once):
        mysql -u root -p < setup_db.sql

    3. Train the ML model (run once):
        python train_model.py

    4. Start the Flask server:
        python main.py
        Visit: http://localhost:5000
"""

from app import app ,db 

if __name__ =='__main__':
    with app .app_context ():
        db .create_all ()
        print ("✅ Database ready.")
    print ("🚀 Starting Soil Crop Prediction System on http://localhost:5000")
    app .run (debug =True ,host ='0.0.0.0',port =5000 )
