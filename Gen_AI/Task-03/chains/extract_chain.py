import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from prompts.extract_prompt import extract_prompt

print("DEBUG GROQ KEY:", os.getenv("GROQ_API_KEY"))

# Initialize LLM
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0
)

# Output parser
parser = StrOutputParser()

# Chain
extract_chain = extract_prompt | llm | parser