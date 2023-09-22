from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .model_rf import AQIPredictorRandomForest
app = FastAPI()
origins = ['http://127.0.0.1:5500']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
predictor = AQIPredictorRandomForest("BENV/air-quality-india.csv")
data = predictor.load_data()
predictor.train_model(data)


@app.get('/{datetime_str}')
def add(datetime_str: str):
    predicted_data_day = predictor.predict_aqi(datetime_str)
    predict_aqi_by_week = predictor.predict_aqi_by_week(datetime_str).tolist() 
    return {
        'predicted_data_day': predicted_data_day,
        'predict_aqi_by_week': predict_aqi_by_week
    }
