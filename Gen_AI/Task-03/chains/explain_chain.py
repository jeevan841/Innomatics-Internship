from langchain_core.output_parsers import StrOutputParser

from prompts.explain_prompt import explain_prompt
from chains.extract_chain import llm  # reuse same LLM

# Output parser
parser = StrOutputParser()

# LCEL chain
explain_chain = explain_prompt | llm | parser