import logging
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import datetime
import matplotlib.pyplot as plt 
from constants import Metrics


class Predictor:
    def __init__(self, use_data_after_date: str = None):
        self.accuracy = None
        self.use_data_after_date = use_data_after_date
        self.predictions = None
        self.metrics = None

    def parse_bookings(self):
        df_rolling = pd.read_csv('bookings.csv', parse_dates=['date','start_time', 'end_time'], index_col=[0])
        df_rolling = df_rolling.drop(['start_time', 'end_time'], axis=1)
        df_rolling[df_rolling > 0] = 1
        df_rolling = df_rolling.reset_index()
        df_rolling['days_since_booked'] = (df_rolling.date - np.roll(df_rolling.date, shift=1))
        df_rolling.days_since_booked = df_rolling.days_since_booked.apply(lambda x: x.days)
        df_rolling.rename(columns={'total_time_hours': 'booked'}, inplace=True)
        # drop first row
        df_rolling = df_rolling.drop(df_rolling.index[0])
        
        df_rolling_filled_dates = df_rolling.set_index('date').resample('D').mean()
        # increment by 1 each day until the next booking    
        for _, row in df_rolling_filled_dates.iterrows():
            if row.booked == 1:
                counter = 1
            else:
                row.days_since_booked = counter
                counter += 1
        df_rolling_filled_dates.replace(np.nan, 0, inplace=True)
        self.data = df_rolling_filled_dates

        # Hack to fix large gap in data when I was away on exchange for 4 months
        if self.use_data_after_date:
            self.data = self.data.loc[self.use_data_after_date:]


    def fit_model(self):
        # Beacuse of uneven distribution of labels, we adjust weights inversely proportional to class frequencies
        self.model = LogisticRegression(class_weight='balanced')
        X, y = self.data.days_since_booked.values.reshape(-1, 1), self.data.booked.values.ravel()
        # split 
        N = len(X)
        self.X_train, self.X_test, self.y_train, self.y_test = X[:int(N*0.8)], X[int(N*0.8):], y[:int(N*0.8)], y[int(N*0.8):]

        self.model.fit(self.X_train, self.y_train)
        self.generate_metrics()

    def generate_metrics(self):
        self.metrics = {
            Metrics.F1_SCORE: f1_score(self.y_test, self.model.predict(self.X_test)),
            Metrics.ACCURACY: self.model.score(self.X_test, self.y_test)
        }

    def predict(self, threshold, look_forward_days=30):
        # get date from the last row of df_rolling_filled_dates
        latest_booking_date = self.data.index[-1].date()

        if latest_booking_date > datetime.date.today():
            logging.info('Laundry slot already booked in the future. No need to compute probability.')
            return
        
        dates_forward = np.array([latest_booking_date + datetime.timedelta(days=i) for i in range(look_forward_days)])
        vals = np.arange(0, look_forward_days).reshape(-1, 1)
        predictions = self.model.predict_proba(vals)[:, 1]

        self.make_figure(dates_forward, predictions)
        self.make_predictions_dict(dates_forward, predictions, threshold)

    def make_predictions_dict(self, dates_forward, preds, threshold):
        print(dates_forward[preds >= threshold])
        if len(preds[preds >= threshold]) == 0:
            logging.info('No predictions above threshold') 
            return
        self.predictions = dict(zip(dates_forward[preds >= threshold], preds[preds >= threshold]))
        return

    def make_figure(self, dates_forward, preds):
        plt.figure(figsize=(12, 10))
        plt.scatter(dates_forward, preds, label='Predicted probability')
        #plt.scatter(vals[y_test==1], y_test[y_test==1], label='actual')
        plt.legend()
        plt.tight_layout()
        plt.savefig('current_predictions.png', dpi=150, bbox_inches="tight")