import time
import psycopg2
import os
from flask import Flask, render_template, url_for, request
from postgres_tools import * 
from analysis_tools import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/table', methods=['GET', 'POST'])
def get_data():

    if request.method == 'POST':

        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        comment = request.form['comment']

        insert_line(";".join([date, amount, category, comment]))

    else:
    	pass
	
    return render_template('index.html', history=read_table_htmlfriendly())
    

@app.route('/analysis', methods=['GET', 'POST'])
def analyse():

    if request.method == 'POST':
        start = request.form['start']
        stop = request.form['stop']
        date_window = request.form['date_window']


        if start and stop and date_window:
            frame_dict = read_table_framefriendly()
            if frame_dict:
                plot_heatmap(frame_dict, start, stop, date_window)

    return render_template('analysis.html')

@app.errorhandler(404)
def not_found(error):
    return '404. Try "GET /" or "GET /health"', 404


if __name__ == "__main__":
	app.run(debug=True)

