from typing import Text
from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask.scaffold import F
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import numpy as np
import pandas as pd 
import os as os 
from fuzzywuzzy import fuzz

df = pd.read_csv('Shortage dataset.csv')
checker = df['Special Condition']
checker.fillna("No special conditions attached", inplace = True)
job_List = df['Job types included on the shortage occupations list']

app = Flask(__name__)

views = Blueprint('views', __name__)


@app.route('/', methods=['GET', 'POST'])
def first_name():
    if request.method == 'POST':
        yourname = request.form.get('yourname')
        answer = yourname
        answer = answer.lower()
        answer = answer.strip()
        score = 0
        best_score = 0
        jobs_title = []
        closest_matching = []
        index = 0 
        closest_index = 0
        for x in job_List:
            score = fuzz.ratio(answer , x)
            jobs_title = [x]
            index = index + 1
            if (score > best_score):
                best_score = score
                closest_matching = jobs_title
                closest_index = index
        if (best_score >= 90):
            if not checker.iloc[closest_index] == "No special conditions attached":
                #Still need to find out how to print out the special condition
                return render_template('special_Conditon.html', timmy=checker.iloc[closest_index])
            else:
                return render_template('result.html')
        #Still need to import the closest matching for this
        if (best_score > 60 and best_score < 90):
            return render_template('close_But_NoCigar.html', gil = closest_matching) 
        else: 
            return render_template('fail.html')

    else:
        return render_template('Index.html')

#Going to need to take two parameters with one being a default value where if it matches default value do not print special condition
#@app.route('/<usr>')
#def user(usr):
 #   return f"<h1>It seems the job you searched for of {usr} is available</h1>"

#@app.route('/<close>')
#def close_Result(close):
#    return f'<h1> it seems your result could be spelt wrong as it is close to somethign'



@app.errorhandler(404)
def page_not_found(e):
    return '<h1>page not found</h1>'


if __name__ == "__main__":
    app.run(debug=True)