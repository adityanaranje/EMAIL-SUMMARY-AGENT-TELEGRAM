from langchain_openai import ChatOpenAI
from config.settings import OPENAI_API_KEY

llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature=0.1,
    api_key=OPENAI_API_KEY
)

def extract_job_info(email_text):

    prompt = f"""
    You are an email analyzer. You have to classify emails as job related or ml ai data science related or other.

    Classify email type:

    JOB
    AI_RELATED
    OTHER

    Return JSON ONLY in this format:

    {{
    "type": "",
    "company": "",
    "role": "",
    "location": "",
    "experience": "",
    "apply_link": "",
    "company_link": "",
    "skills": [],
    "summary": []
    }}

    Rules:
    - skills must list key technologies (Python, NLP, AWS, SQL, LLM etc)
    - summary must contain 2–3 bullet points
    - if not JOB, skills can be empty
    - output must be valid JSON
    - do not include markdown

    Email:
    {email_text}
    """

    response = llm.invoke(prompt)

    return response.content