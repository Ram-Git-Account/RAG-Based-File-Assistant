from langchain_groq import ChatGroq
from prompts import ANSWER_PROMPT

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def generate_answer(context, query):
    prompt = ANSWER_PROMPT.format(context=context, query=query)
    response = llm.invoke(prompt)
    return response.content