from langchain_core.output_parsers import StrOutputParser

from prompts.match_prompt import match_prompt
from chains.extract_chain import llm  # reuse same LLM

# Output parser
parser = StrOutputParser()

# LCEL chain
match_chain = match_prompt | llm | parser