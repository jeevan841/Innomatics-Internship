from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate(
    input_variables=["resume_data", "match_data", "score"],
    template="""
You are an AI assistant explaining candidate evaluation results to a recruiter.

INPUTS:
1. Resume Data (JSON)
2. Matching Analysis (JSON)
3. Score

TASK:
Explain clearly why the candidate received this score.

Your explanation must include:
- Strengths (matching skills)
- Weaknesses (missing skills)
- Experience relevance

STRICT RULES:
- Use ONLY the provided data
- Do NOT assume or hallucinate
- Be factual and concise
- Keep explanation professional and easy to understand

Return output in STRICT JSON format:

{{
  "explanation": ""
}}

Resume Data:
{resume_data}

Matching Data:
{match_data}

Score:
{score}
"""
)