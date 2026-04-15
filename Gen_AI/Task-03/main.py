from dotenv import load_dotenv
load_dotenv()
import os

# 🔍 Enable LangSmith Tracing (MANDATORY)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "LANGSMITH_API_KEY"
os.environ["LANGCHAIN_PROJECT"] = "resume-screening"

# Import chains
from chains.extract_chain import extract_chain
from chains.match_chain import match_chain
from chains.score_chain import score_chain
from chains.explain_chain import explain_chain


# Pipeline Function
def run_pipeline(resume, job_description):
    print("\n🔹 Step 1: Extracting Information...")
    extracted = extract_chain.invoke({
        "resume": resume
    })
    print(extracted)

    print("\n🔹 Step 2: Matching with Job Description...")
    matched = match_chain.invoke({
        "resume_data": extracted,
        "job_description": job_description
    })
    print(matched)

    print("\n🔹 Step 3: Scoring Candidate...")
    score = score_chain.invoke({
        "match_data": matched
    })
    print(score)

    print("\n🔹 Step 4: Generating Explanation...")
    explanation = explain_chain.invoke({
        "resume_data": extracted,
        "match_data": matched,
        "score": score
    })
    print(explanation)

    return {
        "extracted": extracted,
        "match": matched,
        "score": score,
        "explanation": explanation
    }


# Loading Data
with open("data/job_description.txt") as f:
    job_description = f.read()

with open("data/strong.txt") as f:
    strong_resume = f.read()

with open("data/average.txt") as f:
    average_resume = f.read()

with open("data/weak.txt") as f:
    weak_resume = f.read()


# Run for all 3 candidates
print("\n STRONG CANDIDATE")
run_pipeline(strong_resume, job_description)

print("\n AVERAGE CANDIDATE ")
run_pipeline(average_resume, job_description)

print("\nWEAK CANDIDATE ")
run_pipeline(weak_resume, job_description)