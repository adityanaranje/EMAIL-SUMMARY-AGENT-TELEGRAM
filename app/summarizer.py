from langchain_openai import ChatOpenAI
from config.settings import OPENAI_API_KEY

llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature=0.2
)

def summarize_email(email_text):

    prompt = f"""
    Summarize this email in 3 concise bullete points:

    {email_text}
    """

    response = llm.invoke(prompt)

    return response.content