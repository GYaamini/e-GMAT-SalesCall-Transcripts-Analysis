from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

CORS(app)

# MongoDB Config
MONGO_PASSWORD = os.getenv("DB_PASSWORD")
MONGO_USERNAME = os.getenv("DB_USERNAME")
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@clustersct.egh1vbn.mongodb.net/transcripts?retryWrites=true&w=majority&appName=ClusterSCT"

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client.transcripts
mongo_collection = mongo_db.transcript_texts


# SQLite3 Config
sqlite3_db = "SC_Tdb.db"
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(sqlite3_db)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

import routes

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT'))