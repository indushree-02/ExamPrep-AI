import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Load .env
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)


def generate_answer(question, context):

    prompt = f"""
You are an AI Exam Preparation Assistant.

Use ONLY the context below to answer.

If the answer is not present, say:
"I couldn't find this information in the uploaded study material."

Context:
{context}

Question:
{question}

Generate the answer in this format:

Definition

Explanation

Important Exam Points

Related Previous Year Questions (if any)
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content


if __name__ == "__main__":

    context = """
Deadlock is a condition where two or more processes wait forever.
Four conditions:
Mutual Exclusion
Hold and Wait
No Preemption
Circular Wait

2024 PYQ:
Explain Deadlock.
"""

    question = "Explain Deadlock"

    answer = generate_answer(question, context)

    print(answer)