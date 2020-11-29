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
template_path = os.path.join(project_root, './templates/')

app = Flask(__name__)


@app.route('/<name>')
def index(name):
    return render_template('base.html', name=name)

# of percent change, returns date and returns column, pretty self explanatory
@app.route('/CheckPercent/<ticker>/<int:percent>')
def check_percent(ticker, percent):
    df = (pd.DataFrame(TimeSeries(key='FDRKL7ONQ94G1OQB',
                                  output_format='pandas').get_daily_adjusted(ticker, outputsize='full')[0]))
    df["% change"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[abs(df['% change']) >= percent, :]
    finaldf = df_sub[["% change"]].sort_index(ascending=False)
    prefinaldict = finaldf.to_dict()
    a = prefinaldict['% change']
    #a = {}
    # for i in finaldict:
    #    a[str(i)] = finaldict[i]
    return render_template('base.html', a=a)
    # format of a is JSON, passing through a as a

# greater than a certain percent
@app.route('/CheckPercentGreater/<ticker>/<percent>')
def check_percent_greater(ticker, percent):
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df["returns"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[(df['returns']) >= percent, :]
    df_sub[["returns"]].sort_index(ascending=False)
    finaldf = df_sub[["returns"]].sort_index(ascending=False)
    prefinaldict = finaldf.to_dict()
    b = prefinaldict['returns']
    return render_template('sample.html', b=b)
    # format of b is JSON, passing through b as b
    # sample.html is a placeholder, should switched for whichver html is used for formatting

# greater than a certain percent with a timeframe
@app.route('/CheckPercentGreaterTimeframe/<ticker>/<percent>/<start_date>/<end_data>')
def check_percent_greater_by_date(ticker, percent, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub.loc[(df['returns']) >= percent, :]
    finaldf = df_sub[["returns"]].sort_index(ascending=False)
    prefinaldict = finaldf.to_dict()
    finaldict = prefinaldict['returns']
    c = finaldict
    return render_template('sample.html', c=c)
    # format of c is JSON, passing through c as c
    # sample.html is a placeholder, should switched for whichver html is used for formatting

# greater than a certain percent with a timeframe and period
@app.route('/CheckPercentGreaterTimeframePeriod/<ticker>/<n>/<percent>/<start_date>/<end_data>')
def check_percent_greater_by_date_timeframe(ticker, n, percent, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=n)*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub.loc[(df['returns']) >= percent, :]
    finaldf = df_sub[["returns"]].sort_index(ascending=False)
    prefinaldict = finaldf.to_dict()
    finaldict = prefinaldict['returns']
    d = finaldict
    return render_template('sample.html', d=d)
    # format of d is JSON, passing through d as d
    # sample.html is a placeholder, should switched for whichver html is used for formatting

# certain margin around a stock  #all in percentages of 100
@app.route('/CheckPercentChangeMargin/<ticker>/<stock_return>/<margin>')
def percent_change_margin(ticker, stock_return, margin):
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df["returns"] = df["5. adjusted close"].pct_change() * \
        100  # percent change * 100
    df_sub = df[(df["returns"] < stock_return+margin) & (df["returns"]
                                                         > stock_return-margin)]  # defining returns you want
    # sort values by date
    finaldict = df_sub[["returns"]].sort_index(ascending=False).to_dict()
    e = finaldict['returns']
    return render_template('sample.html', e=e)
    # format of e is JSON, passing through e as e
    # sample.html is a placeholder, should switched for whichver html is used for formatting

# certain margin around a stock with set start and end date and period (n) #all in percentages of 100
@app.route('/CheckPercentChangeMarginTimeframePeriod/<ticker>/<n>/<stock_return>/<margin>/<start_date>/<end_date>')
def percent_change_margin_by_date_timeframe(ticker, n, stock_return, margin, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=n)*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub[(df["returns"] < stock_return+margin) &
                    (df["returns"] > stock_return-margin)]  # defining returns you want
    # sort values by date  #sort_values(["returns"])
    finaldict = df_sub[["returns"]].sort_index(ascending=False).to_dict()
    f = finaldict['returns']
    return render_template('sample.html', f=f)
    # format of f is JSON, passing through f as f
    # sample.html is a placeholder, should switched for whichver html is used for formatting

# highest returns with n as amount of rows and timeframe
@app.route('/CheckPercentTopReturns/<ticker>/<n>/<t>/<start_date>/<end_date>')
def top_N_returns(ticker, n, t, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=n)*100
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub.sort_values(["returns"], ascending=False)
    df_sub = df_sub[["returns"]].head(t).to_dict()  # series of the returns
    final_dict = df_sub['returns']
    h = {}
    for i in final_dict:
        a[str(i)] = final_dict[i]
    return render_template('sample.html', g=g)
    # format of e is JSON, passing through e as e
    # sample.html is a placeholder, should switched for whichver html is used for formatting

# lowest returns with n as amount of rows and timeframe
@app.route('/CheckPercentBottomReturns/<ticker>/<n>/<t>/<start_date>/<end_date>')
# lowest returns over a certain period within a certain timeframe
def bottom_N_returns(ticker, n, t, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=n)*100
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub.sort_values(["returns"])
    finaldict = df_sub[["returns"]].head(t).to_dict()
    h = finaldict['returns']
    return render_template('sample.html', h=h)
    # format of h is JSON, passing through h as h
    # sample.html is a placeholder, should switched for whichver html is used for formatting

# annualized returns, volatility, and sharpe over a certain timeframe
@app.route('/ReturnsInfo/<ticker>/<start_date>/<end_date>')
# annualized returns, volatility, and sharpe over a certain timeframe
def return_info(ticker, start_date, end_date):
    # start_date = pd.to_datetime(start_date)
    # end_date = pd.to_datetime(end_date)
    assert pd.to_datetime(start_date) < pd.to_datetime(
        end_date), "start_date must eb less than end_date"  # make sure start date < end date
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]  # 1st input of list
    df = df.sort_index()  # sort based on date
    df["returns"] = df["5. adjusted close"].pct_change() * \
        100  # get percentage change
    df = df.dropna(subset=["returns"])  # drop NA values
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub["returns"]  # series of the returns
    # annulizing number of trading days in a year. average daily return*252
    mean_returns = df_sub.mean()*252
    # volatility is standard deviation of annualized returns*square root of 252, np is numpy library
    volatility = df_sub.std()*np.sqrt(252)
    finaldict = pd.DataFrame({"Annualized Returns": [mean_returns], "Annualized Volatility": [
                             volatility], "Annualized Sharpe": [mean_returns/volatility]}).to_dict()
    return render_template('sample.html', finaldict=finaldict)
    # format of finaldict is JSON, passing through finaldict as finaldict
    # sample.html is a placeholder, should switched for whichver html is used for formatting
    # final dict is composed of three things: Annualized Returns, Annualized Volatility, and Annualized Sharpe Ratio
    # In that order, these 3 things will be the output of the function in a JSON format