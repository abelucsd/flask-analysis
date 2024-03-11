from flask import Blueprint, render_template, request, jsonify
from .models import SampleModel
from . import db
from . import models


from io import StringIO
import json

import pandas as pd
import numpy as np

import collections

analysis = Blueprint('analysis', __name__)

@analysis.route('/analysis', methods=['GET', 'POST'])
def analysis_api():
    # Only 1 file that filled a SampleModel object
    sample = SampleModel.query.all()[0]
    # convert json into table
    sample_json = sample.json_data
    sample_map = json.loads(sample_json)

    return render_template('analysis.html', data = sample_map), 200
    pass
    if request.method == 'POST':
        # collection
        # display bar graph of selected attributes



        # if prediction: must have a y output
        # encode str data to int
        # display distribution of the x attributes
        # select algorithm for prediction
        pass