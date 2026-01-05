from langchain_core.prompts import PromptTemplate

ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["context"],
    template="""
You are evaluating an autonomous agent using UI video evidence.

Tasks:
1. Align planning steps with UI actions
2. Identify deviations or inefficiencies
3. Highlight UI friction
4. Provide recommendations

Context:
{context}

Return a structured professional report.
"""
)
