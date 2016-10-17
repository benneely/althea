# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import sys
import datetime

app = Flask(__name__)
@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter

@app.route("/", methods=['GET'])
def index():
    return render_template('root.html', 
                           title="Althea")

@app.route("/models", methods=['GET','POST'])
def models():
    if request.method == 'GET':
        return render_template('models.html', 
                               my_string="Wheeeee!", 
                               my_list=[0,1,2,3,4,5], 
                               title="Models Available", 
                               current_time=datetime.datetime.now())
    elif request.method == 'POST':
        _model_name = request.form['ModelName']
        _doi        = request.form['DOI']
        _model_response = request.form['Response']
        text = _model_name + " " + _doi + " " + _model_response
        print(request.form)
        return render_template('models.html', 
                               my_string=text, 
                               my_list=[0,1,2,3,4,5], 
                               title="Models Available", 
                               current_time=datetime.datetime.now())
    
@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html', 
                           my_string="Wheeeee!",
                           title="Register a New Model")

def main():
    try:
        port = int(sys.argv[1])
    except:
        port = 8001
    app.run(debug=True,host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()