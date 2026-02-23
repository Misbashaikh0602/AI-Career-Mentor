import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
