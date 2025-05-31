from flask import request, jsonify
from sqlalchemy import or_, cast, func
from sqlalchemy.types import String
import pandas as pd
from app import app, mongo_collection, get_db
import os
import json
import random
from dotenv import load_dotenv
from insight_analysis import transcript_summary, analyze_transcript, fallback_strategy

load_dotenv()

view = os.getenv("SQLITE_TABLEVIEW")
table = os.getenv("SQLITE_TABLE")

# insights_file = "transcripts_insight.json"
insights_file = "transcripts_insight_diffLLM.json"

# summary_file = "transcript_summary.json"
summary_file = "transcript_summary_diffLLM.json"

#########################
# HELPER FUNCTIONS
#########################

def load_local(SUMMARY_local_FILE):
    if os.path.exists(SUMMARY_local_FILE):
        with open(SUMMARY_local_FILE, "r") as f:
            return json.load(f)
    return {}

def save_local(SUMMARY_local_FILE, local):
    with open(SUMMARY_local_FILE,"w") as f:
        json.dump(local, f, indent=2)
        
def populate_insights_summaries(local,rows,query,db_timestamp):
    try:       
        result = []
        if len(rows) > 15:
            rows = random.sample(rows, min(15, len(rows)))
        for row in rows:
            row_dict = dict(row)
            readable = ',\n '.join(f"{k}: {v}" for k, v in row_dict.items())

            # Check if the relevant data already in local storage
            transcript_id = row["transcript_id"]
            
            local_summary = load_local(summary_file)
            if transcript_id in local_summary:
                print(f"Fetched {transcript_id} summary from local storage")
                result.append(local_summary[transcript_id])
            
            else:
                llm_result = transcript_summary(readable)

                # Store the newly fetched data to the local storage
                local_summary = load_local(summary_file)
                local_summary[transcript_id] = llm_result
                save_local(summary_file, local_summary)
                print(f"Fetched {transcript_id} summary from LLM request")
                
                result.append(readable)
        full_text = '\n\n'.join(result)
        
        llm_result = analyze_transcript(full_text, query)
        local[query]["timestamp"] = db_timestamp
        local[query]["analysis"] = llm_result
        
        save_local(insights_file, local)
        print(f"Fetched insights for {query} from LLM request")
        
        return jsonify({"analysis": llm_result})
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


#########################
# ROUTES
#########################

# MongoDB route to get Transcripts Text
@app.route('/get_transcript_text', methods=['POST'])
def get_transcript_text():
    data = request.get_json()
    transcript_id = data.get("col_value")

    doc = mongo_collection.find_one({"transcript_id": transcript_id}, {"_id": 0})
    if doc:
        return jsonify(doc)
    return jsonify({"error": "Not found"}), 404


# SQLite routes to access Transcripts Conversion Likelihood Analysis
@app.route('/get_transcript_data', methods=['POST'])
def get_transcript_data():
    """Get analysis data by transcript_id"""
    db = get_db()
    data = request.get_json()

    col_name = data.get("col_name")
    col_value = data.get("col_value")
    op = data.get("operator")
    
    allowed_operators = ['=', '!=', '<', '<=', '>', '>=']
    if op not in allowed_operators:
        return jsonify({"error": "Invalid operator"}), 400

    if not view or not col_name:
        return jsonify({"error": "Missing view or column name"}), 400

    query = f"SELECT * FROM {view} WHERE {col_name} {op} ? ORDER BY CAST(conversion_likelihood AS FLOAT) DESC"
    cursor = db.execute(query, (col_value,))
    
    print(query, (col_value,))
    
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])

@app.route('/search_transcript_data', methods=['POST'])
def search_transcript_data():
    db = get_db()
    data = request.get_json()

    col_name = data.get("col_name")
    query = data.get("col_value")
    
    if not view or not col_name:
        return jsonify({"error": "Missing view or column name"}), 400

    sql = f"SELECT * FROM {view} WHERE LOWER({col_name}) LIKE ? ORDER BY CAST(conversion_likelihood AS FLOAT) DESC"
    cursor = db.execute(sql, (f"%{query.lower()}%",))
    
    print(sql, (f"%{query}%",))
    
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])


# LLM request endpoint
@app.route('/get_transcript_summary', methods=['POST'])
def get_transcript_summary():
    db = get_db()
    data = request.get_json()

    transcript_id = data.get("col_value")

    if not view or not transcript_id:
        return jsonify({"error": "Missing query parameters"}), 400

    try:
        query = f"SELECT * FROM {table} WHERE transcript_id = ?"
        cursor = db.execute(query, (transcript_id,))
        row = cursor.fetchone()

        row_dict = dict(row)
        readable = ',\n '.join(f"{k}: {v}" for k, v in row_dict.items())

        # Check if the relevant data already in local storage
        transcript_id = row["transcript_id"]
        
        local = load_local(summary_file)
        if transcript_id in local:
            print(f"Fetched {transcript_id} summary from local storage")
            return jsonify({"analysis": local[transcript_id], "local": True})

        llm_result = transcript_summary(readable)

        # Store the newly fetched data to the local storage
        local = load_local(summary_file)
        local[transcript_id] = llm_result
        save_local(summary_file, local)
        print(f"Fetched {transcript_id} summary from LLM request")
            
        return jsonify({"analysis": llm_result})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    

@app.route('/get_analyzed_transcript_data', methods=['POST'])
def get_analyzed_transcript_data():
    data = request.get_json()

    rows = data.get("rows")
    query = data.get("query")

    if not rows:
        return jsonify({"error": "Missing Data"}), 400
    
    # Check if the DB source has changed data
    db_path = "SC_Tdb.db"
    db_timestamp = os.path.getmtime(db_path)
    
    local = load_local(insights_file)
    if query not in local.keys():
        local[query] = {}
        return populate_insights_summaries(local,rows,query,db_timestamp)
        
    elif db_timestamp > local[query]["timestamp"]:
        return populate_insights_summaries(local,rows,query,db_timestamp)
    
    else:
        try:
            insight = local.get(query).get('analysis')
            print(f"Fetched insights for {query} from local storage")
            return jsonify({"analysis": insight, "local": True})

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    

@app.route('/get_fallback_strategy_for_insights', methods=['POST'])
def insights_fallback_strategy():
    data = request.get_json()

    insights = data.get("insights")
    query = data.get("query")

    if not insights:
        return jsonify({"error": "Missing Data"}), 400

    local = load_local(insights_file)
    if query not in local.keys():
        return jsonify({"analysis": "Fetch analysis before reaching for strategies"})
    
    try:
        if 'strategy' in local.get(query).keys():
            print(f"Fetched strategy for {query} from local storage")
            return jsonify({"analysis": local[query]["strategy"], "local": True})
        
        llm_result = fallback_strategy(insights, query)
        local[query]["strategy"] = llm_result
            
        save_local(insights_file, local)
        print(f"Fetched strategy for {query} from LLM request")
            
        return jsonify({"analysis": llm_result})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500