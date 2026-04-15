from langchain_core.prompts import PromptTemplate

match_prompt = PromptTemplate(
    input_variables=["resume_data", "job_description"],
    template="""
You are an AI assistant helping a recruiter evaluate candidates.

Your task is to compare the candidate profile with the job description.

INPUTS:
1. Resume Data (structured JSON)
2. Job Description

TASK:
- Identify matching skills
- Identify missing skills
- Evaluate overall alignment

STRICT RULES:
- Only use information explicitly present in resume_data
- Do NOT assume or infer skills
- Do NOT hallucinate
- Be objective and precise

Return output in STRICT JSON format:

{{
  "matching_skills": [],
  "missing_skills": [],
  "match_summary": ""
}}

Resume Data:
{resume_data}

Job Description:
{job_description}
"""
)