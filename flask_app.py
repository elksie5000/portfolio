# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from dash import Dash, html
import dash
# Removed this because couldn't get protobuf solution to work
#from google.cloud import bigquery
from flask_sqlalchemy import SQLAlchemy
import os
import dash_core_components as dcc
from dash.dependencies import Input, Output
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/service-account-file.json'
import dash_vega_components as dvc
#https://stackoverflow.com/questions/55023231/importerror-no-module-named-flask-ext
#from sqlalchemy import Column, Float, Integer, String
#import flask.ext.restless
import pandas as pd
import altair as alt
import dataset
pd.options.display.max_colwidth = 5000
pd.options.display.max_rows = 600
from sqlalchemy.orm import sessionmaker


#import requests
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from shapely.geometry import Point, shape
#import json
import pandas as pd



app = Flask(__name__)
app.secret_key = 'This is really unique and secret'

app.debug = True

#app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}?ssl_disabled=true".format(
    username="elksie5000",
    password="lest_nearby_salami_slight",
    hostname="elksie5000.mysql.pythonanywhere-services.com",
    databasename="elksie5000$skynet",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

engine = create_engine(SQLALCHEMY_DATABASE_URI)


Session = sessionmaker(bind=engine)
session = Session()
try:
    database = dataset.connect(SQLALCHEMY_DATABASE_URI)
except:
    print ("couldn't connect to database")

@app.route('/')
def hello_world():
    return render_template('index3.html')

@app.route('/tic-tac-toe')
def tic_tac():
    return render_template('tictactoe.html')

@app.route('/articles')
def article_page():
    return render_template('articles.html')




@app.route('/portfolio')
def article_portfolio():
    return render_template('portfolio.html')

@app.route("/war_dead")
def war_dead():
    return render_template("war_dead.html")

@app.route("/war_dead_panels")
def war_dead_panels():
    return render_template("war_dead_panels.html")

@app.route("/crime_map")
def crime_map():
    return render_template("crime_map.html")

#from flask_app import app as application


dash_app = Dash(__name__, server=app, url_base_pathname='/babies/')  # Use the existing Flask app as the server
# Create ten input fields for names
# Create ten input fields for names
name_inputs = [dcc.Input(id=f'name-input-{i}', type='text', placeholder=f'Enter name {i}') for i in range(1, 11)]

dash_app.layout = html.Div([
    *name_inputs,
    dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'Male', 'value': 'boy'},
            {'label': 'Female', 'value': 'girl'}
        ],
        value='M'
    ),
    dcc.Dropdown(
        id='measure-dropdown',
        options=[
            {'label': 'Rank', 'value': 'Rank'},
            {'label': 'Count', 'value': 'Count'}
        ],
        value='Rank'
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            dvc.Vega(
                id="chart",
                opt={"renderer": "svg", "actions":False},
                spec={},  # Initialize with an empty spec
            )
        ]
    )
])


@dash_app.callback(
    Output('chart', 'spec'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State(f'name-input-{i}', 'value') for i in range(1, 11)] + [dash.dependencies.State('gender-dropdown', 'value'), dash.dependencies.State('measure-dropdown', 'value')]
)
def update_chart(n_clicks, *args):
    if n_clicks > 0:
        try:
            #Load the baby names
            with engine.connect() as connection:
                df = pd.read_sql("SELECT Name from baby_names;", engine)
                names = df['Name'].unique().tolist()
            names = args[:10]  # Get the first ten arguments, which are the names
            gender = args[10]  # The eleventh argument is the gender
            measure = args[11]  # The twelfth argument is the measure

            charts = []
            for i, name in enumerate(names):
                if name:  # Only fetch data if a name is given
                    with engine.connect() as connection:
                        data = pd.read_sql("SELECT * FROM baby_names WHERE name = %s and gender = %s and Measure = %s;", connection, params=(name, gender, measure))
                    if not data.empty:
                        # Create a selection that updates based on the point that the user is hovering over
                        hover = alt.selection_single(on='mouseover', nearest=True, empty='none')

                        # Create a chart for the data
                        line = alt.Chart(data).mark_line().encode(
                            x='Year:Q',
                            y='Value:Q',
                            color=alt.condition(hover, alt.value('red'), alt.value('lightgray')),  # Change the color based on the hover selection
                            tooltip=['Name:N', 'Value:Q'],  # Show a tooltip with the name and value
                            # Add a legend
                            detail='name:N'
                        ).add_selection(
                            hover  # Add the hover selection to the chart
                        )

                        points = alt.Chart(data).mark_point(points=True).encode(
                            x='Year:Q',
                            y='Value:Q',
                            color=alt.condition(hover, alt.value('red'), alt.value('lightgray')),  # Change the color based on the hover selection
                            tooltip=['Name:N', 'Value:Q']  # Show a tooltip with the name and value
                        ).add_selection(
                            hover  # Add the hover selection to the chart
                        )

                        chart = line + points
                        charts.append(chart)

            if not charts:
                return {"title": "No data found for the given names, gender, and measure."}

            # Combine all charts
            chart = alt.layer(*charts)

            return chart.to_dict()
        except Exception as e:
            return {"title": f"An error occurred: {str(e)}"}
    else:
        raise PreventUpdate  # Don't update the chart if the button hasn't been clicked

"""
@app.route("/nationals")
def scrape_nationals():
    feeds = [{"type": "news","title": "BBC", "url": "http://feeds.bbci.co.uk/news/uk/rss.xml"},
        {"type": "news","title": "The Economist", "url": "https://www.economist.com/international/rss.xml"},
        {"type": "news","title": "The New Statesman", "url": "https://www.newstatesman.com/feed"},
        {"type": "news","title": "The New York Times", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
        {"type": "news","title": "Metro UK","url": "https://metro.co.uk/feed/"},
        {"type": "news", "title": "Evening Standard", "url": "https://www.standard.co.uk/rss.xml"},
        {"type": "news","title": "Daily Mail", "url": "https://www.dailymail.co.uk/articles.rss"},
        {"type": "news","title": "Sky News", "url": "https://news.sky.com/feeds/rss/home.xml"},
        {"type": "news", "title": "The Mirror", "url": "https://www.mirror.co.uk/news/?service=rss"},
        {"type": "news", "title": "The Sun", "url": "https://www.thesun.co.uk/news/feed/"},
        {"type": "news", "title": "Sky News", "url": "https://news.sky.com/feeds/rss/home.xml"},
        {"type": "news", "title": "The Guardian", "url": "https://www.theguardian.com/uk/rss"},
        {"type": "news", "title": "The Independent", "url": "https://www.independent.co.uk/news/uk/rss"},
        #{"type": "news", "title": "The Telegraph", "url": "https://www.telegraph.co.uk/news/rss.xml"},
        {"type": "news", "title": "The Times", "url": "https://www.thetimes.co.uk/?service=rss"}]
    print(feeds)

    data = []                               # <---- initialize empty list here
    for feed in feeds:
        parsed_feed = feedparser.parse(feed['url'])
        #print("Title:", feed['title'])
        #print("Number of Articles:", len(parsed_feed.entries))
        #print("\n")
        for entry in parsed_feed.entries:

            title = entry.title
            print(title)
            url = entry.link
            #print(entry.summary)
            try:
                summary = entry.summary[:400] or "No summary available" # I simplified the ternary operators here
            except:
                #print("no summary")
                summary = "none"
            try:
                date = pd.to_datetime(entry.published)#
                #or "No data available"     # I simplified the ternary operators here
            except:
                #print("date")
                date = pd.to_datetime("01-01-1970")
            data.append([title, url, summary, date])          # <---- append data from each entry here

    df = pd.DataFrame(data, columns = ['title', 'url', 'summary', 'date'])
    articles = pd.read_sql('nationals', con = engine)
    articles = articles.drop_duplicates()
    df = df.append(articles)
    df = df.drop_duplicates()
    df.to_sql('nationals', con = engine, if_exists = 'replace', index = False)
"""
