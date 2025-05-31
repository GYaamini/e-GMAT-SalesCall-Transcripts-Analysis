
import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API Setup
OPENROUTER_API_KEY = os.getenv('API_KEY')
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# LLM Function
def transcript_summary(transcript):
    # model="meta-llama/llama-3.3-8b-instruct:free"
    model="deepseek/deepseek-r1-0528-qwen3-8b"
    
    prompt = f"""e-GMAT is a popular online platform for GMAT (Graduate Management Admission Test) preparation. 
        It's known for its personalized study plans, extensive video lessons, and AI-powered diagnostic tools, 
        making it a valuable resource for test takers seeking to improve their scores.
        e-GMAT agents has their sales calls with prospect candidates to understand the prospect's performance in GMAT
        so far and their goals. The agents then lay down the study plan for them to achieve target goals and 
        explain the product features. Lastly they discuss on product pricing and wrap up the call Q&A session and
        the chances of prospect opting to purchase the product i.e., likelihood of conversion. 

        Here is the list of data keys - what they indicate that are derived from sales call transcripts that 
        needs to be summarized:
        transcript_id - Transcription identifier, month - Month of Sales call, conversion_likelihood - likelihood of
        prospect candidate purchasing the product, reasoning - Reasons supporting the likelihood, 
        emotions_detected - Overall emotions, location - Location either pertaining to residence or target business
        school, education - Prospect's education background, organization - Organization either pertaining to 
        prospect's current workplace, or prospect's alma mater or the target business school, date - Relevant dates, 
        agent_emotions_with_score - Sales agent emotions in each sales call phase and it's intensity, 
        agent_duration - Count of sales agent talking turns in each call phase, agent_keywords - Sales agent most 
        used keywords in each call phase, prospect_emotions_with_score - Prospect emotions in each sales call phase 
        and it's intensity, prospect_duration - Count of prospect talking turns in each call phase, 
        prospect_keywords - Prospect most used keywords in each call phase, start_end_time - Time frame of each call
        phase, agent_vs_prospect_num - Ratio of agent vs prospect talking turns in each call phase
        
        Here is the data for Context:
        {transcript}:
        
        Here is the 7 major phases that will be mentioned:
        Introduction, Prospect’s performance, Agent drawing up plan, Explaining product, Price discussion, Q&A, Wrap
        
        Summarize the given Context on the the basis of its effect on Conversion Likelihood (Mean conversion 
        likelihood is 0.55) by following the given instruction.
        
        Instructions:
        1. Use correlation and Context Reasoning 
        2. Consider all the related keys for a cohesive summarization
        3. Use information like location, education, organization, etc to describe Prospect's background
        4. Use information like most frequent keywords used in Price discussion, Q&A phase or agent vs prospect num 
            to determine the factors influencing the conversion likelihood.
        4. Give a brief and precise summary of few lines on the provided data
        5. DO NOT create data and DO NOT hallucinate the summaries and conclusions
        6. The format should be:
            Transcript identifier:\n
            Summary: your output
        
        Summary:
    """

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1  # More deterministic for analysis
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            data=json.dumps(payload)
        )
        print("open router response done")
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return "Something went wrong :("


def analyze_transcript(merged_text, query):
    model="anthropic/claude-3.5-sonnet"
    # model="meta-llama/llama-3.3-8b-instruct:free"
    
    prompt = f"""e-GMAT is a popular online platform for GMAT (Graduate Management Admission Test) preparation. 
        It's known for its personalized study plans, extensive video lessons, and AI-powered diagnostic tools, 
        making it a valuable resource for test takers seeking to improve their scores.
        e-GMAT agents has their sales calls with prospect candidates to understand the prospect's performance in GMAT
        so far and their goals. The agents then lay down the study plan for them to achieve target goals and 
        explain the product features. Lastly they discuss on product pricing and wrap up the call Q&A session and
        the chances of prospect opting to purchase the product i.e., likelihood of conversion. 
        
        Here is the list of transcript summaries as Context for the given conditional query - {query}:
        {merged_text}
        
        Analyze the given Context and draw insights on the Conversion Likelihood (Mean conversion 
        likelihood is 0.55):
        If most likelihood are weak (less than mean likelihood) in the provided summary list,then your analysis 
        should be: 
            1. Which set of characteristics (like frequently used reasoning, or emotional intensity status, or 
                agent vs prospect talk duration, etc across similar likelihood sales calls) and 
                what kind of agent-prospect engagement resulted in weak conversion likelihood? (give insights with 
                appropriate group of transcript identifiers where these characteristics are observed)
            2. List the key factors and reasons with justification like
                    Positives:
                    Drawbacks:
            3. What changes should be considered to increase the conversion likelihood?
        If most likelihood are strong (more than mean likelihood) then your analysis should be:
            1. Which set of characteristics (like frequently used reasoning, or emotional intensity status, or 
                agent vs prospect talk duration, etc across similar likelihood sales calls) and 
                what kind of agent-prospect engagement resulted in more conversion? (give insights with appropriate 
                group of transcript identifiers where these characteristics are observed)
            3. List the key factors and reasons with justification like
                Positives:
                Drawbacks:
            4. What approach should be considered to improve the conversion likelihood?
        
        Why there is distinct difference between the prospects who are most likely to purchase the product and the 
        ones that won't (difference seen between summaries with min and max conversion likelihood) and what affects 
        this phenomenon? (like location, education, organization, etc demographic factors or frequently used 
        reasoning across similar likelihood sales calls)
        
        Instructions:
        1. You are a Data Analyst and is an expert in extracting insights from textual and numerical data
        2. Use correlation and Context Reasoning 
        3. Give detailed yet brief insight on the provided data and be precise
        4. DO NOT create data and DO NOT hallucinate the summaries and conclusions
        5. List only major insights that are affecting the purchase likelihood
        6. Use information like location, education, organization, etc from summaries to describe Prospect's 
            background and whether that demography has any affect on conversion likelihood.
        7. Use information like most frequent keywords used in Price discussion, Q&A phase or agent vs prospect num 
            to determine the factors influencing the conversion likelihood.
        8. Format your findings with suitable question key for each insight block
        9. The format should be:
            Query: provided conditional query\n
            Analysis: your output
        
        Analysis:
    """

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1  # More deterministic for analysis
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            data=json.dumps(payload)
        )
        print("open router response done")
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return "Something went wrong :("


def fallback_strategy(insights, query):
    model="mistralai/ministral-8b"
    # model="meta-llama/llama-3.3-8b-instruct:free"
    
    prompt = f"""e-GMAT is a popular online platform for GMAT (Graduate Management Admission Test) preparation. 
        It's known for its personalized study plans, extensive video lessons, and AI-powered diagnostic tools, 
        making it a valuable resource for test takers seeking to improve their scores.
        e-GMAT agents has their sales calls with prospect candidates to understand the prospect's performance in GMAT
        so far and their goals. The agents then lay down the study plan for them to achieve target goals and 
        explain the product features. Lastly they discuss on product pricing and wrap up the call Q&A session and
        the chances of prospect opting to purchase the product i.e., likelihood of conversion. 

        Here is the analyzed insights of e-GMAT Sales call transcripts as analysis for the given conditional 
        query - {query}:
        {insights}
        
        Go through the given analysis on the Conversion Likelihood with its current strengths and weaknesses and come
        up with strategies to retain the current purchase likelihood trend or to improve/increase the purchase 
        likelihood of the prospects:
        
        Instructions:
        1. You are an expert business strategist with marketing and sales knowledge to boost product sales
        2. Provide upto 15 strategic moves that caters to specific issues found in the provided analysis
        3. Use correlation and Context Reasoning 
        4. Be detailed and precise
        4. DO NOT create data and DO NOT hallucinate the summaries and conclusions
        5. Format your strategies and its justification in points
        
        Strategies:
    """

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1  # More deterministic for analysis
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            data=json.dumps(payload)
        )
        print("open router response done")
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return "Something went wrong :("
