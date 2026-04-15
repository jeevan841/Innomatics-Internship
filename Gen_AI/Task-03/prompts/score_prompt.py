from langchain_core.prompts import PromptTemplate

score_prompt = PromptTemplate(
    input_variables=["match_data"],
    template="""
You are an AI system responsible for scoring a candidate based on job fit.

INPUT:
Matching Analysis (JSON):
{match_data}

TASK:
Assign a score between 0 and 100 based on the following criteria:

SCORING RULES:
- Strong Match (most skills match, few missing) → 80–100
- Moderate Match (some key skills missing) → 50–79
- Weak Match (many important skills missing) → 0–49

ADDITIONAL RULES:
- Base your score ONLY on the provided matching data
- Do NOT assume any additional skills
- Be consistent and logical
- Avoid randomness

Return output in STRICT format:

{{
  "score": number
}}
"""
)