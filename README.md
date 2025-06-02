# 📞 e-GMAT Sales Call Transcripts Analysis

**Boosting Sales Conversion with Data & AI**

|          Condition Based Data Retrieval   |   Cumulative Insight Analysis    |
| -------------------- | --------------------- |
| ![Analysis UI 1](https://github.com/user-attachments/assets/57540057-45b1-4612-90cc-bce78c42ec80)   | ![Analysis UI 1](https://github.com/user-attachments/assets/d171ae13-f58a-4009-869b-2bdefc1fe26c)    |

---
# 📃 Contents

1. Transcripts Annotation with Speaker target variable and Speaker Classification
2. Call phase and Emotions Segmentation with Transformers, Keyword extraction with NLP
3. Conversion Rate Analysis using Emotion, Engagement & Clarity
4. React + Flask Web Interface for Review & Strategy Access
5. Hybrid Database Design with SQLite3 & MongoDB
6. AI-Driven Follow-Up Strategy with Multi-LLM Insights

---
# ✨ Features

* **Speaker Classification**: Transformer-based segmentation of agent vs prospect
* **Emotion & Engagement Analysis**: Multilabel emotion detection using BERT (GoEmotions)
* **Heuristic Phase Detection**: Segment calls into Planning, Product Explanation, Q\&A, etc.
* **Keyword & Entity Extraction**: Using YAKE and SpaCy NER for contextual insights
* **Conversion Hypothesis Testing**: Statistical and anecdotal validation of success factors
* **Dashboard with Conversion Heatmaps**: Phase-wise analysis, conversion likelihoods, demographics
* **Multi-Model LLM Strategy**: Smart routing across Claude, DeepSeek, Mistral, and LLaMA
* **File-Caching LLM Outputs**: Query- and call-based cache to minimize latency and cost

---
# 📊 Key Insights

## Conversion Drivers

```bash
✔ Positive emotions during Q&A & wrap-up phases = higher conversion
✔ Prospect determination during performance talks = better outcome
✔ Agent confidence and clarity during explanation & pricing = key
✔ Balanced speaking ratio, prospect engagement = critical
```

## Findings

```bash
🔸 Agent-to-Prospect Speaking Ratio: Weak correlation (r = +0.028)
🔸 Positive Prospect Emotion in Wrap-up: Strong signal of conversions
🔸 Education Background: CS/Engineering/Postgrad prospects convert more
🔸 Seasonal Trends: GMAT prep months show conversion spikes
```

## Phase Impact

```bash
🔹 Planning & Product Explanation → Clarity driven
🔹 Performance, Q&A & Wrap-Up → Engagement & emotion driven
🔹 Pricing Phase → Most predictive of outcome
```

---
# 🧠 AI-Powered Follow-Up System

## Strategy Highlights

* **Emotion-Aware AI-Driven Selling**: Real-time emotion tracking + Automated Study Plan
* **Demo-First Experience**: Personalized product videos, interactive trials
* **Segmented Marketing**: Tailored follow-ups based on education, location, & behavior
* **Incentive Optimization**: Seasonal offers, scholarships, early-bird discounts
* **Post-Call Automation**: Summaries, reminders, dashboards, and feedback loops

## ⚙️ LLM Selection per Task

| Task                 | Preferred Model       | Reason                      |
| -------------------- | --------------------- | --------------------------- |
| Transcript Summaries | DeepSeek R1 Qwen3-8B  | Best structure, conciseness |
| Insight Generation   | Claude 3.5 Sonnet     | Better abstraction          |
| Strategy Suggestions | Mistral 8B            | Actionable outputs          |
| Budget Option        | LLaMA 3.3 8B Instruct | Fast and cheap, but generic |

---
# ⚙️ Tech Stack

`Python` `BERT` `PyTorch` `React (Vite)` `Flask` `SQLite3` `MongoDB` `YAKE` `SpaCy` `LLMs: DeepSeek, Claude, Mistral, LLaMA`

---
## Setup & Run

1. Clone the repository
2. Navigate to the project directory

   ```bash
   cd e-GMAT-SalesCall-Transcripts-Analysis
   ```

3. Frontend Setup

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Backend Setup

   ```bash
   cd ../backend
   python3 -m venv venv
   venv\Scripts\activate   ## on MacOS and Linux : source venv/bin/activate
   pip install -r requirements.txt
   flask run
   ```

---
# To-Do / Enhancements

* Annotate more dataset and perform extensive training and testing
* Expand emotion training data to improve accuracy in ambiguous segments

---
# Acknowledgments
Thanks to e-GMAT for the challenge, the dataset and LLM APIs powered by OpenRouter.

---
