import os
import streamlit as st
from groq import Groq

# Read from Streamlit secrets first, fallback to local env
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

client = Groq(api_key=api_key)
def ask_llm(question):

    system_prompt = """
You are an AI Career Mentor.

Your job:
- Guide students about careers
- Suggest skills, tools, technologies
- Explain learning paths
- Be clear, structured, and practical
- Give step-by-step advice

Do NOT give cybersecurity-only answers.
Answer according to the user's career question.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content
