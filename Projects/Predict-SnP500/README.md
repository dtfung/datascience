##S&P500 Price Predictions

Predict future prices using historical data on the price of the S&P500 Index.  Predicting whether an index will go up or down will help us forecast how the stock market as a whole will perform.  Since stocks tend to correlate with how well the economy as a whole is performing, it can also help us to make economic forecasts.  This project uses data from the [S&P500 Index](https://en.wikipedia.org/wiki/S%26P_500_Index).  The dataset was taken from [here](https://www.quandl.com/data/YAHOO/INDEX_GSPC-S-P-500-Index).

##Installation

* Install the requirements using `pip install -r requirements.txt`

##Usage

* Run `python predict.py`
    * This will create a processed dataset, training and test data
    * The data will then be fitted, trained, tested and evaluated
    * The mean absolute error and R-squared metrics will be printed

##Extending this

If you want to extend this work, here are a few places to start:

* Generate more features and perform feature selection.
    * Use the `assembly.py` file to add them to the dataset
    * Use the `features.py` to perform the necessary calculations
    * Add the name of the feature to a list called `features` found in `settings.py`
    * Here are some suggested features:
        1. The average volume over the last 5 days
        2. The average volume over the last 30 days
        3. The average volume over the past year
        4. The ratio between the average volume for the past 5 days and the average volume over the past year
        5. The standard deviation of the average volume over the last 5 days
        6. The standard deviation of the average volume over the last 30 days
        7. The standard deviation of the average volume over the past year
        8. The ratio between the standard deviation of the average volume for the past 5 days and the standard deviation of the average volume over the past year
        9. The year component of the date.
        10. The month component of the date.
        11. The day of week.
        12. The day component of the date.
        13. Market news
* Try new models in `predict.py`
* Make predictions on live data
* Make predictions on individual stocks





