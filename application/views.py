from flask import Blueprint, render_template
from .models import SampleModel
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html'), 200

@views.route('/view')
def api_view():
    """
        View page for the Sample API

        Parameters:
        url route

        Returns:
        template and HTTPResponse
    """
    # Only 1 file that filled a SampleModel object
    sample = SampleModel.query.all()[0]
    # convert json into table
    sample_json = sample.json_data
    sample_map = json.loads(sample_json)

    # deconstruct map and create table -- table is the map

    return render_template("view.html", table=sample_map), 200