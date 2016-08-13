##Predicting Boston Housing Prices

A supervised learning project


###Description

As part of the Machine Learning Engineer Nanodegree program, this first project was about building a model to accurately predict the prices of a client’s home in the Greater Boston Area.  I was provided with a dataset from the UCI Machine Learning Repository (https://archive.ics.uci.edu/ml/datasets/Housing) that contains samples of 506 houses in the suburbs of Boston.  I used a Decision Tree, a supervised learning model used for both classification and regression type problems, to make a prediction on the price of the client's home.  
The dataset was partitioned into training and testing sets, then fitted to the Decision Tree.  The key metric was the mean absolute error between the model's predicted house values and the actual values of the houses in the datset.  GridSearchCV was used to find the optimal depth of the Decision Tree.

###Software and Libraries:

- Python 2.7
- NumPy
- scikit-learn
- matplotlib
- iPython Notebook
