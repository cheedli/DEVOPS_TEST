from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import requests

app = Flask(__name__)
CORS(app)
BACKEND_URL = 'https://backend.themenufy.com/product/retrieve'

def fetch_data():
    try:
        # Fetch data from the backend URL
        response = requests.get(BACKEND_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Convert response to JSON
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to prepare data for model training
def prepare_data(df):
    X = df[['price']]
    y = df['score']  # Combined score to predict
    return X, y

# Class for the recommendation model based on linear regression
class LinearRecommender:

    def __init__(self, df):
        self.df = df
        self.model = None
        self.mae = None
        self.mse = None
        self.r2 = None

    def train(self):
        # Prepare data
        self.df['score'] = self.df['price']  # Assuming the price is used for scoring

        # Prepare data for model training
        X, y = prepare_data(self.df)

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize linear regression model
        self.model = LinearRegression()

        # Train the model
        self.model.fit(X_train, y_train)

        # Predict on test set
        y_pred = self.model.predict(X_test)

        # Calculate metrics
        self.mae = mean_absolute_error(y_test, y_pred)
        self.mse = mean_squared_error(y_test, y_pred)
        self.r2 = r2_score(y_test, y_pred)

        print(f"MAE of the linear regression model is: {self.mae}")
        print(f"MSE of the linear regression model is: {self.mse}")
        print(f"R2 score of the linear regression model is: {self.r2}")

    def recommend_top_products(self, top_n=25):
        # Prepare data for the full set
        X, _ = prepare_data(self.df)

        # Predict scores for all products
        self.df['score'] = self.model.predict(X)

        # Sort products by score
        self.df = self.df.sort_values('score', ascending=False)

        # Select top recommended products
        top_products = self.df[['name', 'photo', 'description', 'price']].head(top_n)

        return top_products

# Fetch data from backend URL
data = fetch_data()
if data:
    print("Fetched data:", data)  # Print fetched data to inspect its structure
    df = pd.DataFrame(data)
    print("DataFrame columns:", df.columns)  # Print DataFrame columns to ensure they are correct

    # Ensure the dataframe contains all necessary columns
    if 'price' not in df.columns:
        print("Error: 'price' column not found in the data")
    else:
        if 'score' not in df.columns:
            df['score'] = df['price']  # Assuming the price is used for scoring

        # Initialize the recommendation model with the fetched dataset
        recommender_linear = LinearRecommender(df)

        # Train the linear regression model
        recommender_linear.train()

        # Get the top recommended products
        top_products_linear = recommender_linear.recommend_top_products()

        # Endpoint to get recommendations
        @app.route('/', methods=['GET'])
        @cross_origin()

        def get_recommendations():
            return jsonify(top_products_linear.to_dict(orient='records'))


        @app.route('/prod', methods=['GET'])
        @cross_origin()

        def get_recommendations():
            return jsonify(top_products_linear.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2233, debug=True)
