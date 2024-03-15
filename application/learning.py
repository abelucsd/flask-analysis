from flask import Blueprint, render_template, request, jsonify
from .models import SampleModel
from . import db
from . import models


from io import StringIO
import json

import collections

# Data
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
# from xgboost import XGBRegressor
# from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

learning = Blueprint('learning', __name__)

@learning.route('/learning', methods=['GET', 'POST'])
def learning_api():
    # Only 1 file that filled a SampleModel object
    sample = SampleModel.query.all()[0]
    # convert json into table
    sample_json = sample.json_data
    sample_map = json.loads(sample_json)
    print(type(sample))

    if request.method == 'POST':
        for item in request.form:
            print(item)
        print(request.form['learning_algo'])

        learning_algo = request.form['learning_algo']

        # TODO:
        # - X and Y into dataframes.
        # - Train Test Split

        # Train and Test Data
        # Use random_state: 42
        
                
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state=2)

        if learning_algo.lower() == 'linear regression':
            pass
        elif learning_algo.lower() == 'ensembles':
            pass
        elif learning_algo.lower() == 'neural network':
            pass


    

    return render_template('learning.html', data = sample_map), 200