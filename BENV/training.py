from model_rf import AQIPredictorRandomForest

predictor = AQIPredictorRandomForest("BENV/air-quality-india.csv")
data = predictor.load_data()
predictor.train_model(data)
predictor.save_model("model.pkl")