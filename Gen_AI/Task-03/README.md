# Innomatics-Internship

# 🧠 AI Resume Screening System with Explainability & Tracing

An AI-powered system that evaluates resumes against job descriptions using LangChain, providing structured scoring and human-readable explanations.

---

## 🚀 Overview

This project demonstrates how Large Language Models (LLMs) can be orchestrated into a real-world system for recruitment.

The system:
- Extracts structured information from resumes
- Matches candidates with job requirements
- Assigns a score (0–100)
- Explains the reasoning behind the score
- Tracks the entire pipeline using LangSmith

---

## 🎯 Features

✔ Modular LangChain pipeline (LCEL)  
✔ Skill extraction from unstructured resumes  
✔ Matching logic with job description  
✔ Rule-based scoring system  
✔ Explainable AI outputs  
✔ LangSmith tracing & debugging  
✔ Secure API handling using `.env`  

---

## 🧩 System Architecture

Resume → Extraction → Matching → Scoring → Explanation

---

## 🛠️ Tech Stack

- Python  
- LangChain (LCEL)  
- Groq API (LLM inference)  
- LangSmith (Tracing & Debugging)  
- dotenv (Environment Management)  

---

## 📂 Project Structure
resume-screening-ai/\n
│
├── prompts/\n
│ ├── extract_prompt.py\n
│ ├── match_prompt.py\n
│ ├── score_prompt.py\n
│ └── explain_prompt.py\n
│
├── chains/\n
│ ├── extract_chain.py\n
│ ├── match_chain.py\n
│ ├── score_chain.py\n
│ └── explain_chain.py\n
│
├── data/\n
│ ├── strong.txt\n
│ ├── average.txt\n
│ ├── weak.txt\n
│ └── job_description.txt\n
│
├── main.py\n
├── requirements.txt\n
├── .env (not included)\n
└── README.md\n
\n
---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/jeevan841/Innomatics-Internship/tree/main/Gen_AI/Task-03.git
cd Task-03
```

## Install dependencies:

pip install -r requirements.txt

Environment Setup

Create a .env file:

GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=resume-screening

unning the Project
python main.py
