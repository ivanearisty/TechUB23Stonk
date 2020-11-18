from flask import Flask, render_template
import feedparser
import random
import time
from datetime import datetime, timezone, timedelta
import pandas as pd
import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'