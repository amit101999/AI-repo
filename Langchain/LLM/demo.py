import Langchain_openai import openAI
from dotenv import load_dotenv

load_dotenv()

llm = openAI(model="gpt-3.5-turbo")

result = llm("What is the capital of France?")
print(result)