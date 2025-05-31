import json
import os
from app import mongo_collection, mongo_client
from pymongo import ReplaceOne

try:
    mongo_client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas!")
    
    filepath = os.path.join(os.getcwd().split('backend')[0],"e-GMAT_SalesCall_DataAnalysis_80","transcript_texts_80.json")
    with open(filepath) as f:
        transcripts = json.load(f)

    operations = [
        ReplaceOne({"transcript_id": t["transcript_id"]}, t, upsert=True)
        for t in transcripts
    ]

    # Execute in bulk
    if operations:
        result = mongo_collection.bulk_write(operations)
        print("Bulk write result:", result.bulk_api_result)
    else:
        print("No operations to perform.")
        
except Exception as e:
    print("❌ Failed to connect:", e)
