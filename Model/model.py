import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
import seaborn as sns

class AQIPredictor:
    def __init__(self, data_file) -> None:
        self.data_file = data_file
        self.regr = LinearRegression()
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
        df['Timestamp'] = (df["Timestamp"].apply(AQIPredictor.convert_to_datetime) - self.reference_date).dt.total_seconds()
        return df

    def train_model(self, df) -> LinearRegression:
        x = np.array(df["Timestamp"]).reshape(-1, 1)
        y = np.array(df["PM2.5"]).reshape(-1, 1)
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)
        self.regr.fit(xtrain, ytrain)
        return self.regr

    @staticmethod
    def convert_to_datetime(date_str: str) -> datetime:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return pd.to_datetime(date_obj.strftime("%Y-%m-%d %H"))

    def predict_aqi(self, datetime_str) -> np.ndarray:
        datetime_obj = pd.to_datetime(datetime_str)  # Call as a static method
        timestamp = datetime_obj.timestamp()
        predicted_aqi = self.regr.predict(np.array([[timestamp]]))
        return predicted_aqi[0][0]

if __name__ == '__main__':
    data_file = "SIH Project/air-quality-india.csv"
    predictor = AQIPredictor(data_file)

    data = predictor.load_data()
    predictor.train_model(data)

    input_datetime = '2023-09-17 12'
    predicted_aqi = predictor.predict_aqi(input_datetime)
    print(f'Predicted AQI for {input_datetime}: {predicted_aqi}')
