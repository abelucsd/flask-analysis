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
    # print(type(sample))

    if request.method == 'POST':
        print(request.form)
        # for item in request.form:
        #     print(item)
        # print(request.form['dep-1'])
        # print(request.form['learning_algo'])
        
        # for item in request.data:
        #     print(item)

        # print(request.form)

        import time
        time.sleep(20)

        return render_template('learning.html', data = {'sample_map': sample_map}), 200
        

        # Y value is last
        import re
        learning_algo = request.form['learning_algo']
        # fill X and Y
        x_attrs, y_attr = [], ''
        for key in request.form:
            if key.startswith('indep-'):
                x_attrs.append(key)
            elif key.startswith('dep-'):
                # only 1 occurence of y output
                y_attr = key

        # TODO:
        # - X and Y into dataframes.
        # - Train Test Split

        # Train and Test Data
        # Use random_state: 42
        X = sample_map.drop([y_attr])
        Y = sample_map[y_attr]
                
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state=42)

        ml_model = None
        train_data_pred, test_data_pred = [], []
        error_score, error_score_test = 0, 0
        if learning_algo.lower() == 'linear regression':
            ml_model = LinearRegression()

            # Fit the model
            ml_model.fit(X_train, Y_train)
            train_data_pred = ml_model.predict(X_train)
            error_score = metrics.r2_score(Y_train, train_data_pred) # r squared error
            ml_model.score(X_test, Y_test)
            mean_squared_error(ml_model(X_train), Y_train, squared=False)

            # Test Data            
            
            test_data_pred = ml_model.predict(X_test)
            error_score_test = metrics.r2_score(Y_test, test_data_pred)
            mean_squared_error(ml_model(X_test), Y_test, squared=False)

            # Build context data for template

            # reformat learning.html for data -> data.sample_map jinja code.
            ctx = {'y_test': Y_test, 'y_pred': test_data_pred, 'model_type': learning_algo, 'sample_map': sample_map}
            return render_template('learning.html', data = ctx), 200

            pass
        elif learning_algo.lower() == 'ensembles':
            pass
        elif learning_algo.lower() == 'neural network':
            pass        

    return render_template('learning.html', data = {'sample_map': sample_map}), 200