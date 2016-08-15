##Stock Price Prediction

Predict the price of any S&P500 company.  The software is built to take in a single company, and train a linear regression model for predictions.  It is currently set to make predictions based on daily trading data retrieved from [here](https://www.quandl.com/data/YAHOO/INDEX_GSPC-S-P-500-Index).  

##Installation

* Install the requirements using `pip install -r requirements.txt`

##Requirements:

* pandas
* matplotlib
* scikit-learn
* numpy
* ipython
* scipy

##Usage

* Run `python predict.py`
    * This will create a processed dataset
    * Train, test and predict on stock data
    * Prints mean absolute error on training and testing target data

##Extending This

If you want to extend this work, here are a few places to start:

* Optimize feature selection to reduce error in price predictions
* Train the model to predict price data for several companies simultaneously
* Fit live stock data to the model 
* Build a mobile or web application to accept user input
    * user could select from a list of stocks
    * specify a date range to retrieve data
    * specify trading frequency (seconds, minutes, hours, 1 day, 5 days, 30 days etc.)

