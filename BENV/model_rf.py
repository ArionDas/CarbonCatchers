from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime
import pandas as pd
import numpy as np

class AQIPredictorRandomForest:
    def __init__(self, data_file) -> None:
        self.data_file = data_file
        self.rf_regr = RandomForestRegressor(n_estimators=100, random_state=0)
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

    def predict_aqi(self, datetime_str) -> np.ndarray:
        datetime_obj = pd.to_datetime(datetime_str)
        timestamp = datetime_obj.timestamp()
        predicted_aqi = self.rf_regr.predict(np.array([[timestamp]]))
        return predicted_aqi[0]
    
    def predict_aqi_by_week(self, datetime_str, noise_level=5.0) -> np.ndarray:
        datetime_obj = pd.to_datetime(datetime_str)
        timestamp = datetime_obj.timestamp()
        timestamps = np.array([timestamp - 3 * 24 * 3600, timestamp - 2 * 24 * 3600,
                                timestamp - 1 * 24 * 3600, timestamp,
                                timestamp + 1 * 24 * 3600, timestamp + 2 * 24 * 3600,
                                timestamp + 3 * 24 * 3600]).reshape(-1, 1)
        predicted_val = self.rf_regr.predict(timestamps)
        noise = np.random.normal(0, noise_level, predicted_val.shape)
        predicted_val_with_noise = predicted_val + noise
        return predicted_val_with_noise

# Usage
if __name__ == '__main__':
    data_file = "BENV/air-quality-india.csv"
    predictor = AQIPredictorRandomForest(data_file)
    data = predictor.load_data()
    predictor.train_model(data)
    print(predictor.predict_aqi_by_week("2023-09-20 15"))
