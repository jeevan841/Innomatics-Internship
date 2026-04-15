from langchain_core.output_parsers import StrOutputParser

from prompts.score_prompt import score_prompt
from chains.extract_chain import llm  # reuse same LLM

# Output parser
parser = StrOutputParser()

# LCEL chain
score_chain = score_prompt | llm | parser
