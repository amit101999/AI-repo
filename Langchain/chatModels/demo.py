# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# load_dotenv()

# chat = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview")

# result = chat.invoke("What is the capital of France?")
# print(result)


#  now with the huggingface hub
from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint
from dotenv import load_dotenv
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id =  "TinyLlama/TinyLlama-1.1B-Chat-v1.0" ,
     task = "text-generation"
)

result = llm.invoke("What is the capital of France?")
print(result.content)