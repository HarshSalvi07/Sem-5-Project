from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=1.0
)

prompt = ChatPromptTemplate.from_template(
    "Analyze this student performance data and give useful suggestions:\n\n{data}"
)

chain = prompt | llm

with open("data/sample_student_data.csv", "r") as f:
    data = f.read()

response = chain.invoke({"data": data})

print("=== Analysis Result ===")
print(response.content)