from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
You are an AI system designed to extract structured information from resumes.

Your task is to extract ONLY the information explicitly mentioned in the resume.

Extract the following:
1. Skills (technical + soft skills if mentioned)
2. Tools / Technologies
3. Years of Experience (only if clearly stated)

STRICT RULES:
- Do NOT assume or infer missing information
- Do NOT add skills that are not explicitly mentioned
- If something is missing, return an empty list or null
- Be factual and precise

Return output in STRICT JSON format:

{{
  "skills": [],
  "tools": [],
  "experience": ""
}}

Resume:
{resume}
"""
)