import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)


def create_context(chunks):
    """
    Combine retrieved chunks into a single context string.
    """

    return "\n\n".join(chunks)


def generate_answer(question, context):
    """
    Generate an exam-oriented answer using the retrieved context.
    """

    prompt = f"""
You are ExamPrep AI, an expert academic assistant.

Answer the student's question ONLY using the provided context.

If the answer is not present in the context, reply:

"I couldn't find this information in the uploaded study material."

Context:
{context}

Question:
{question}

Generate the answer in the following format:

Definition

Explanation

Important Exam Points

Related Previous Year Questions (if available)
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content


if __name__ == "__main__":

    chunks = [
        """
Deadlock is a condition where two or more processes wait forever.

Four conditions:
1. Mutual Exclusion
2. Hold and Wait
3. No Preemption
4. Circular Wait
""",
        """
2024 PYQ

Q1. Explain Deadlock.
"""
    ]

    context = create_context(chunks)

    answer = generate_answer(
        "Explain Deadlock",
        context
    )

    print("\n")
    print(answer)