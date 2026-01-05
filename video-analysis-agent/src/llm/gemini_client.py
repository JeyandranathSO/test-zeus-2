from langchain_google_genai import ChatGoogleGenerativeAI
from llm.prompts import ANALYSIS_PROMPT

def run_gemini_analysis(context, model, temperature):
    llm = ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key="AIzaSyCLL5au3Yyd-2004GL8Av7Bsc64hFf34uA"
    )
    chain = ANALYSIS_PROMPT | llm
    return chain.invoke({"context": context}).content
