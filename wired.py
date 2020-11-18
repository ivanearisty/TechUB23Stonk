from flask import Flask, render_template
import feedparser
import random
import time
from datetime import datetime, timezone, timedelta
import pandas as pd
import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime as dt
import requests

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/CheckPercent')
def check_percent(ticker, percent): #same as function above but only returns date and returns column 
    df = (pd.DataFrame(TimeSeries(key='FDRKL7ONQ94G1OQB', output_format='pandas').get_daily_adjusted(ticker, outputsize='full')[0]))
    df["% change"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[abs(df['% change']) >= percent,:]
    return df_sub[["% change"]].sort_index(ascending= False)