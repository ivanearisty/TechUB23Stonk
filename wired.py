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

# of percent change, returns date and returns column


@app.route('/CheckPercent')
def check_percent(ticker, percent):
    df = (pd.DataFrame(TimeSeries(key='FDRKL7ONQ94G1OQB',
                                  output_format='pandas').get_daily_adjusted(ticker, outputsize='full')[0]))
    df["% change"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[abs(df['% change']) >= percent, :]
    return df_sub[["% change"]].sort_index(ascending=False)

# greater than a certain percent


@app.route('/CheckPercentGreater')
def check_percent_greater(ticker, percent):
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df["returns"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[(df['returns']) >= percent, :]
    return df_sub[["returns"]].sort_index(ascending=False)

# greater than a certain percent with a timeframe


@app.route('/CheckPercentGreaterTimeframe')
def check_percent_greater_by_date(ticker, percent, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change()*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub.loc[(df['returns']) >= percent, :]
    return df_sub[["returns"]].sort_index(ascending=False)

# greater than a certain percent with a timeframe and period


@app.route('/CheckPercentGreaterTimeframePeriod')
def check_percent_greater_by_date_timeframe(ticker, n, percent, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=n)*100
    df_sub = df.loc[start_date:end_date]
    df_sub = df_sub.loc[(df['returns']) >= percent, :]
    # return df_sub[["returns"]].sort_index()
    return df_sub[["returns"]].sort_index(ascending=False)

# certain margin around a stock  #all in percentages of 100


@app.route('/CheckPercentChangeMargin')
def percent_change_margin(ticker, stock_return, margin):
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df["returns"] = df["5. adjusted close"].pct_change() * \
        100  # percent change * 100
    df_sub = df[(df["returns"] < stock_return+margin) & (df["returns"]
                                                         > stock_return-margin)]  # defining returns you want
    # sort values by date  #sort_values(["returns"])
    return df_sub[["returns"]].sort_index()

# certain margin around a stock with set start and end date and period (n) #all in percentages of 100


@app.route('/CheckPercentChangeMarginTimeframePeriod')
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
    return df_sub[["returns"]].sort_index(ascending=False)

# highest returns with n as amount of rows and timeframe


@app.route('/CheckPercentTopReturns')
def top_N_returns(ticker, n, t, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=n)*100
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub.sort_values(["returns"], ascending=False)
    return df_sub[["returns"]].head(t)  # series of the returns

# lowest returns with n as amount of rows and timeframe


@app.route('/CheckPercentBottomReturns')
def bottom_N_returns(ticker, n, t, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(end_date)
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]
    df = df.sort_index()
    df["returns"] = df["5. adjusted close"].pct_change(periods=n)*100
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub.sort_values(["returns"])
    return df_sub[["returns"]].head(t)  # series of the returns

# annualized returns, volatility, and sharpe over a certain timeframe
@app.route('/ReturnsInfo')
def return_info(ticker, start_date, end_date):
    assert pd.to_datetime(start_date) < pd.to_datetime(
        end_date), "start_date must eb less than end_date"  # make sure start date < end date
    df = TimeSeries(key='HY5IIUWSUZSBEEU5', output_format='pandas').get_daily_adjusted(
        ticker, outputsize='full')[0]  # 1st input of list
    df = df.sort_index()  # sort based on date
    df["returns"] = df["5. adjusted close"].pct_change() * 100  # get percentage change
    df = df.dropna(subset=["returns"])  # drop NA values
    df_sub = df.loc[start_date:end_date]  # slice of date frame
    df_sub = df_sub["returns"]  # series of the returns
    # annulizing number of trading days in a year. average daily return*252
    mean_returns = df_sub.mean()*252
    # volatility is standard deviation of annualized returns*square root of 252, np is numpy library
    volatility = df_sub.std()*np.sqrt(252)
    return pd.DataFrame({"Annualized Returns": [mean_returns], "Annualized Volatility": [volatility], "Annualized Sharpe": [mean_returns/volatility]})
