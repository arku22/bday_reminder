from flask import Flask, render_template
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    conn = psycopg2.connect(database=os.environ.get("database_name"),
                            user=os.environ.get("database_user"),
                            password=os.environ.get("database_user_password"),
                            host=os.environ.get("database_host"),
                            port=os.environ.get("database_port"))

    # read sql query to query database
    with open(Path(Path(__file__).parents[0], "assets/sql/get_event_reminders.sql"), 'r') as f:
        sql_query = f.read()
    df = pd.read_sql_query(sql_query, conn)

    df["event_date"] = pd.to_datetime(df["event_date"], format="%m-%d").dt.date
    df["event_date"] = df["event_date"].apply(lambda x: x.replace(year=2023))

    return render_template("index.html", rows=df.to_dict(orient='records'), columns=df.columns.to_list())
