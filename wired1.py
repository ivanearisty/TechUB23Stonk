from flask import Flask, render_template, request, jsonify, abort
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
import json
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', name="/")


@app.route('/margin')
def margin():
    return render_template('margin.html', name="/")

@app.route('/greaterthan')
def greaterthan():
    return render_template('greaterthan.html', name="/")

@app.route('/lessthan')
def lessthan():
    return render_template('lessthan.html', name="/")  

@app.route('/topreturns')
def topreturns():
    return render_template('topreturns.html', name="/")  

@app.route('/bottomreturns')
def bottomreturns():
    return render_template('bottomreturns.html', name="/")  

@app.route('/sharpe')
def sharpe():
    return render_template('sharpe.html', name="/")  

    return dictionarytest



@app.route('/greaterthanData', methods=["GET", "POST"])
def greater_than_data(name=""):
    if request.method == "POST":
        json_data = request.get_json(force=True) 
        print(json_data)
        print(type(json_data))
        json_data = json.loads(json_data) # convert string to json
        response_date = check_percent_greater_by_date_timeframe(json_data["ticker"], int(json_data["interval"]), float(json_data["percent_change"]), json_data["start_date"], json_data["end_date"])
        response_date_formated = [{"Date":date.replace(" 00:00:00", ""), "Percent Change": round(value ,2)}  for date, value in response_date.items()] 
        return jsonify(response_date_formated)
    else:
        abort(404)

# greater than a certain percent within a timeframe and period n 
#@app.route('/CheckPercentGreaterTimeframePeriod/<ticker>/<int:n>/<float:percent_change>/<start_date>/<end_date>') # works
def check_percent_greater_by_date_timeframe(ticker, interval, percent_change, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=interval)*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub.loc[(df['returns']) >= percent_change, :]
    # return df_sub[["returns"]].sort_index()
    df_sub = df_sub[["returns"]].sort_index(ascending=False).to_dict()
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a

@app.route('/lessthanData', methods=["GET", "POST"])
def less_than_data(name=""):
    if request.method == "POST":
        json_data = request.get_json(force=True) 
        print(json_data)
        print(type(json_data))
        json_data = json.loads(json_data) # convert string to json
        response_date = check_percent_less_by_date_timeframe(json_data["ticker"], int(json_data["interval"]), float(json_data["percent_change"]), json_data["start_date"], json_data["end_date"])
        response_date_formated = [{"Date":date.replace(" 00:00:00", ""), "Percent Change": round(value ,2)}  for date, value in response_date.items()] 
        return jsonify(response_date_formated)
    else:
        abort(404)

# greater than a certain percent within a timeframe and period n 
#@app.route('/CheckPercentLessTimeframePeriod/<ticker>/<int:n>/<float:percent_change>/<start_date>/<end_date>') # works
def check_percent_less_by_date_timeframe(ticker, interval, percent_change, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=interval)*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub.loc[(df['returns']) <= percent_change, :]
    # return df_sub[["returns"]].sort_index()
    df_sub = df_sub[["returns"]].sort_index(ascending=False).to_dict()
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a

@app.route('/marginData', methods=["GET", "POST"])
def margin_data(name=""):
    if request.method == "POST":
        json_data = request.get_json(force=True) 
        print(json_data) # just a dict
        print(type(json_data))
        json_data = json.loads(json_data) # convert string to json
        response_date = percent_change_margin_by_date_timeframe(json_data["ticker"], int(json_data["interval"]), float(json_data["percent_change"]),  float(json_data["margin"]), json_data["start_date"], json_data["end_date"])
        response_date_formated = [{"Date":date.replace(" 00:00:00", ""), "Percent Change": round(value ,2)}  for date, value in response_date.items()] 
        return jsonify(response_date_formated)
    else:
        abort(404)

# certain margin around a stock within a timeframe and period n 
#@app.route('/CheckPercentChangeMarginTimeframePeriod/<ticker>/<int:n>/<float:percent_change>/<float:margin>/<start_date>/<end_date>') # works
def percent_change_margin_by_date_timeframe(ticker, interval, percent_change, margin, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=interval)*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub[(df["returns"] < percent_change+margin) &
                    (df["returns"] > percent_change-margin)]  # defining returns you want
    # sort values by date  #sort_values(["returns"])
    df_sub = df_sub[["returns"]].sort_index(ascending=False).to_dict()
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a

@app.route('/topreturnsData', methods=["GET", "POST"])
def top_returns_data(name=""):
    if request.method == "POST":
        json_data = request.get_json(force=True) 
        print(json_data) # just a dict
        print(type(json_data))
        json_data = json.loads(json_data) # convert string to json
        response_date = top_N_returns(json_data["ticker"], int(json_data["interval"]), int(json_data["number_of_returns"]), json_data["start_date"], json_data["end_date"])
        response_date_formated = [{"Date":date.replace(" 00:00:00", ""), "Percent Change": round(value ,2)}  for date, value in response_date.items()] 
        return jsonify(response_date_formated)
    else:
        abort(404)

# highest returns within a certain timeframe over a certain interval
#@app.route('/CheckPercentTopReturns/<ticker>/<int:n>/<int:t>/<start_date>/<end_date>')
def top_N_returns(ticker, interval, number_of_returns, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=interval)*100
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub.sort_values(["returns"], ascending=False)
    df_sub = df_sub[["returns"]].head(number_of_returns).to_dict() # series of the returns 
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a

@app.route('/bottomreturnsData', methods=["GET", "POST"])
def bottom_returns_data(name=""):
    if request.method == "POST":
        json_data = request.get_json(force=True) 
        print(json_data) # just a dict
        print(type(json_data))
        json_data = json.loads(json_data) # convert string to json
        response_date = bottom_N_returns(json_data["ticker"], int(json_data["interval"]), int(json_data["number_of_returns"]), json_data["start_date"], json_data["end_date"])
        response_date_formated = [{"Date":date.replace(" 00:00:00", ""), "Percent Change": round(value ,2)}  for date, value in response_date.items()] 
        return jsonify(response_date_formated)
    else:
        abort(404)


# lowest returns within a certain timeframe over a certain interval
#@app.route('/CheckPercentBottomReturns/<ticker>/<int:n>/<int:t>/<start_date>/<end_date>')
def bottom_N_returns(ticker, interval, number_of_returns, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=interval)*100
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub.sort_values(["returns"])
    df_sub = df_sub[["returns"]].head(number_of_returns).to_dict()  # series of the returns
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a

@app.route('/sharpeData', methods=["GET", "POST"])
def sharpe_data(name=""):
    if request.method == "POST":
        json_data = request.get_json(force=True) 
        print(json_data) # just a dict
        print(type(json_data))
        json_data = json.loads(json_data) # convert string to json
        response_date = return_info(json_data["ticker"], float(json_data["risk_free_rate"]), json_data["start_date"], json_data["end_date"])
        response_date_formated = [{"Statistic":label, "Value": JSON.stringify(value)}  for label, value in response_date.items()] 
        return jsonify(response_date_formated)
    else:
        abort(404)

# annualized returns, volatility, and sharpe over a certain timeframe
#@app.route('/ReturnsInfo/<ticker>/<start_date>/<end_date>')
def return_info(ticker, risk_free_rate, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(
        end_date), "start_date must eb less than end_date"  # make sure start date < end date
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]  # 1st input of list
    df = df.sort_index()  # sort based on date
    df["returns"] = df["5. adjusted close"].pct_change() * 100  # get percentage change
    df = df.dropna(subset=["returns"])  # drop NA values
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub["returns"]  # series of the returns
    # annulizing number of trading days in a year. average daily return*252. risk free rate of 3%
    mean_returns = round((df_sub.mean()*252), 2)
    risk_free = risk_free_rate
    # volatility is standard deviation of annualized returns*square root of 252, np is numpy library
    volatility = round(df_sub.std()*np.sqrt(252), 2)
    final_dict = pd.DataFrame({"Annualized Returns": [mean_returns], "Annualized Volatility": [volatility], "Annualized Sharpe": [(mean_returns-risk_free)/volatility]}).to_dict()
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a


def percent_change_margin_new(ticker, stock_return, margin):
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df["returns"] = df["5. adjusted close"].pct_change()*100  # percent change * 100
    df_sub = df[(df["returns"] < stock_return+margin) & (df["returns"]
                                                         > stock_return-margin)]  # defining returns you want
    # sort values by date  #sort_values(["returns"])
    df_sub = df_sub[["returns"]].sort_index(ascending=False).to_dict()
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a


# greater than a certain percent 
@app.route('/CheckPercentGreater/<ticker>/<float:percent>')# works
def check_percent_greater(ticker, percent):
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df["returns"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[(df['returns']) >= percent, :]
    df_sub = df_sub[["returns"]].sort_index(ascending=False)
    df_sub = df_sub.to_dict()
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a
    

# greater than a certain percent within a timeframe
@app.route('/CheckPercentGreaterTimeframe/<ticker>/<float:percent>/<start_date>/<end_date>') # works
def check_percent_greater_by_date(ticker, percent, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub.loc[(df['returns']) >= percent, :]
    df_sub = df_sub[["returns"]].sort_index(ascending=False).to_dict()
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a



# certain margin around a stock  
@app.route('/CheckPercentChangeMargin/<ticker>/<float:stock_return>/<float:margin>') # works
def percent_change_margin(ticker, stock_return, margin):
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df["returns"] = df["5. adjusted close"].pct_change()*100  # percent change * 100
    df_sub = df[(df["returns"] < stock_return+margin) & (df["returns"]
                                                         > stock_return-margin)]  # defining returns you want
    # sort values by date  #sort_values(["returns"])
    df_sub = df_sub[["returns"]].sort_index(ascending=False).to_dict()
    final_dict = df_sub['returns']
    a = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return a
    







    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
