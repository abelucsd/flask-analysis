from flask import Blueprint, render_template, request, jsonify
from .models import SampleModel
from . import db
from . import models


from io import StringIO
import json

import pandas as pd
import numpy as np
import re

import collections

api = Blueprint('api', __name__)

@api.route('/api', methods=['GET', 'POST'])
def sample_api():
    """
        Sample API

        Parameters:
        url route
        methods: GET, POST request

        Returns
        Get: template and HTTPResponse
        Get: json data and HTTPResponse
    """

    if request.method == 'GET':
        # data = [row.serialize() for row in SampleModel.query.all()]
        # always only 1 file given which filled the SampleModel.
        try:            
            data = SampleModel.query.all() # [row.serialize() for row in SampleModel.query.all()]
        except AssertionError as e:
            return jsonify(msg='Error: {} '.format(e)), 400

        # if len(data) > 0:
        #     data = SampleModel.query.all()[0]
        # else:
        #     e = 'Please provide a data file.'
        #     return jsonify(msg='Error: {} '.format(e)), 400
        data = SampleModel()
        return render_template('api.html', title="page",jsonfile=data.json_data), 200        

    elif request.method == 'POST':
        """
            Receives data file and insert the data into the database.
            TODO: Feature to add train and test data.
        """
        # TODO: Make sure to only accept XML or txt files.
        print("Submitted a File.")      
                        
        print(request.stream)
        if 'file' not in request.files:
            print("not in request files")       
        
        sample_file_data = request.files['file']        

        # check format
        # if request.content_type != 'text/xml':
        #     error = 'content type must be text/xml. Received {}'.format(request.content_type)
        #     return jsonify(msg='Error: {}. '.format(error)), 400
        
        if not sample_file_data:
            error = "No file input."
            return jsonify(msg='Error: {}. '.format(error)), 400
            
        if sample_file_data:
            df = pd.read_csv(sample_file_data, sep=r"\t|,")

            # check non delimited tab
            # if we get NaN values, then we have a non tab delimited cell
            # if df.isnull().values.any():
            #     error = "Non delimited tabs exist."
            #     return jsonify(msg='Error: {}. '.format(error)), 400
            
            # replace all white space with NaN
            df.replace(r'^\s*$', np.nan, regex = True, inplace=True)

            # drop rows with NULL values
            # df.dropna(inplace = True) TODO: Make this an option.
            # replace nan values to ""
            df.replace(np.nan, "", regex=True, inplace=True)
            
            # data cleaning - remove column leading and trailing whitespace
            df.rename(columns=lambda x: x.strip(), inplace=True)

            # TODO: Delete prior table data            
            SampleModel.query.delete()
            db.session.commit()

            # TODO: Create hashmap, then convert it to json                        
            sample_map = collections.defaultdict(list)
            
            for index, row in df.iterrows():                              
                
                for col_name in df.columns:     
                    if str(row[col_name]).isspace():
                        print("hi there")
                    sample_map[col_name].append(row[col_name])
                    # sample_map[col_name] += ", " + str(row[col_name])
            print("num rows: {}".format(len(df)))
            print(sample_map)
            
            # done - with hashmap data
            # convert to json
            sample_json = json.dumps(sample_map)
                        
            # TODO: Store json into the database
            new_sample = SampleModel(json_data = sample_json)
            try:
                db.session.add(new_sample)                        
            except AssertionError as e:
                return jsonify(msg='Error: {}. '.format(e)), 400
            db.session.commit()

        # Only 1 file given which filled a SampleModel object.
        try:            
            response_data = SampleModel.query.all()[0] # [row.serialize() for row in SampleModel.query.all()]
        except AssertionError as e:
            return jsonify(msg='Error: {} '.format(e)), 400
    
        return response_data.json_data, 201