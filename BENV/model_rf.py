from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime
import pandas as pd
import numpy as np
import pickle as pk
 
class AQIPredictorRandomForest:
    def __init__(self, data_file) -> None:
        self.data_file = data_file
        self.rf_regr = RandomForestRegressor(n_estimators=100, random_state=0, max_depth=10)
        self.reference_date = datetime(2017, 11, 7, 12)

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_file)
        df.dropna(inplace=True)
        convert_dict = {
            "Year": int,
            "Month": int,
            "Day": int,
            "Hour": int,
            "PM2.5": float
        }
        df = df.astype(convert_dict)
        df['Timestamp'] = (df["Timestamp"].apply(AQIPredictorRandomForest.convert_to_datetime) - self.reference_date).dt.total_seconds()
        return df

    def train_model(self, df) -> RandomForestRegressor:
        x = np.array(df["Timestamp"]).reshape(-1, 1)
        y = np.array(df["PM2.5"]).ravel()
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)
        self.rf_regr.fit(xtrain, ytrain)
        return self.rf_regr

    @staticmethod
    def convert_to_datetime(date_str: str) -> datetime:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return pd.to_datetime(date_obj.strftime("%Y-%m-%d %H"))
    
    @classmethod
    def predict_aqi_by_week(cls, regr: RandomForestRegressor, datetime_str, noise_level=5.0) -> np.ndarray:
        datetime_obj = pd.to_datetime(datetime_str)
        timestamp = datetime_obj.timestamp()
        timestamps = np.array([timestamp - 3 * 24 * 3600, timestamp - 2 * 24 * 3600,
                                timestamp - 1 * 24 * 3600, timestamp,
                                timestamp + 1 * 24 * 3600, timestamp + 2 * 24 * 3600,
                                timestamp + 3 * 24 * 3600]).reshape(-1, 1)
        predicted_val = regr.predict(timestamps)
        noise = np.random.normal(0, noise_level, predicted_val.shape)
        predicted_val_with_noise = predicted_val + noise
        return predicted_val_with_noise
    
    def save_model(self, filename):
        with open(filename, 'wb') as file:
            pk.dump(self.rf_regr, file)
    
    @classmethod
    def load_model(cls, filename):
        with open(filename, 'rb') as file:
            return pk.load(file)
        
    @classmethod
    def predict_aqi(cls, regr: RandomForestRegressor, datetime_str):
        datetime_obj = pd.to_datetime(datetime_str)
        timestamp = datetime_obj.timestamp()
        predicted_aqi = regr.predict(np.array([[timestamp]]))
        return predicted_aqi[0]

# Usage
if __name__ == '__main__':
    data_file = "BENV/air-quality-india.csv"
    predictor = AQIPredictorRandomForest(data_file)
    data = predictor.load_data()
    predictor.train_model(data)
    predictor.save_model("BENV/model.pkl")
    new_predictor = AQIPredictorRandomForest.load_model("BENV/model.pkl")
    print(AQIPredictorRandomForest.predict_aqi(new_predictor, "2023-09-20 15"))
