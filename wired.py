from flask import Flask, render_template
import feedparser
import random
import time
from datetime import datetime, timezone, timedelta
import pandas as pd
import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__, template_folder=template_path)

@app.route('/recents')



def rng():
    
    #url = 'https://www.wired.com/feed/rss'

    #listobject = []

    #parsed = feedparser.parse(url)
    #makes now equal to the date and time at which the rss feed was last updated
    #now = datetime.strptime(parsed['channel']['updated'], '%a, %d %b %Y %H:%M:%S +0000')

    #iterating through the items
    #for feed in parsed.entries:
        # setting colors on python not html
    #    setRed = False
    #    publishedDate = datetime.strptime(feed.published, '%a, %d %b %Y %H:%M:%S +0000')
    #    difference = now - publishedDate
    #    if difference.seconds < 3600 and difference.days == 0:
    #        setRed = True
    #    #passing and apending objects for html file
    #    listobject.append({'title':feed.title,'description':feed.description,'published':feed.published, "red":setRed})
    return 7