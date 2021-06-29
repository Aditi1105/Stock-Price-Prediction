from flask_login import UserMixin
from . import db
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from datetime import date
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Predict:
    def check_stock(st_name):
        try:
            df = web.DataReader(st_name, data_source='yahoo', start='2016-01-01', end=date.today())
            # Create a new dataframe with only the 'Close' column

            plt.figure(figsize=(16, 8))
            plt.title('Close Price History')
            plt.plot(df['Close'])
            plt.xlabel('Date', fontsize=18)
            plt.ylabel('Close Price USD ($)', fontsize=18)
            #plt.show()
            plt.savefig('project/static/images/plot1.png')
            data = df.filter(['Close'])
            # Converting the dataframe to a numpy array
            dataset = data.values
            # Get /Compute the number of rows to train the model on
            training_data_len = math.ceil(len(dataset) * .8)
            # Scale all of the data to be values between 0 and 1
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(dataset)
            # Create the scaled training data set
            train_data = scaled_data[0:training_data_len, :]
            # Split the data into x_train and y_train data sets
            x_train = []
            y_train = []
            for i in range(60, len(train_data)):
                x_train.append(train_data[i - 60:i, 0])
                y_train.append(train_data[i, 0])
            # Convert x_train and y_train to numpy arrays
            x_train, y_train = np.array(x_train), np.array(y_train)
            # Reshape the data into the shape accepted by the LSTM
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
            # Build the LSTM network model
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(LSTM(units=50, return_sequences=False))
            model.add(Dense(units=25))
            model.add(Dense(units=1))
            # Compile the model
            model.compile(optimizer='adam', loss='mean_squared_error')
            # Train the model
            model.fit(x_train, y_train, batch_size=1, epochs=1)

            # Test data set
            test_data = scaled_data[training_data_len - 60:, :]
            # Create the x_test and y_test data sets
            x_test = []
            y_test = dataset[training_data_len:,
                     :]  # Get all of the rows from index 1603 to the rest and all of the columns (in this case it's only column 'Close'), so 2003 - 1603 = 400 rows of data
            for i in range(60, len(test_data)):
                x_test.append(test_data[i - 60:i, 0])
            # Convert x_test to a numpy array

            x_test = np.array(x_test)
            # Reshape the data into the shape accepted by the LSTM
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
            # Getting the models predicted price values
            predictions = model.predict(x_test)
            predictions = scaler.inverse_transform(predictions)  # Undo scaling

            # Plot/Create the data for the graph
            train = data[:training_data_len]
            valid = data[training_data_len:]
            valid['Predictions'] = predictions
            # Visualize the data
            plt.figure(figsize=(25, 12))
            plt.title('Model')
            plt.xlabel('Date', fontsize=18)
            plt.ylabel('Close Price USD ($)', fontsize=18)
            plt.plot(train['Close'])
            plt.plot(valid[['Close', 'Predictions']])
            plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
            plt.savefig('project/static/images/plot2.png')
            return "STOCK FOUND"
        except:
            return "Stock not found."
    def pred(self, df):

        return