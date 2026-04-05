from langchain_huggingface import HuggingFaceEndpoint , ChatHuggingFace
from dotenv import load_dotenv
from langchain.core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "google/flan-t5-xxl",
    task = "text2text-generation",
)

model = ChatHuggingFace(llm=llm)

template1 = PromptTemplate(
    template = "What is the capital of {Topic}?",
    input_variables = ['Topic']
)

template2 = PromptTemplate(
    template = "Write a detailed report about {Topic}?",
    input_variables = ['Topic']
)

prompt1 = template1.invoke(Topic = "India")
model_response1 = model.invoke(prompt1)
print(model_response1)

prompt2 = template2.invoke(Topic = "India")
model_response2 = model.invoke(prompt2)
print(model_response2)

# string outut parser 

parser = StrOutputParser()
chain = template1 | model | parser | template2 | model | parser
chain_invoke = chain.invoke(Topic = "India")
print(chain_invoke)