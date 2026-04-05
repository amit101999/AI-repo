from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt1 = PromptTemplate(
    template = "What is the capital of {Topic}?"
    input_variables = ["Topic"]
)


prompt2= PromptTemplate(
    template = "give me a summary of {text}?"
    input_variables = ["text"]
)

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.9)
parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser
# this will create  a sequential chain where the output of one step is passed as input to the next step.
# this is sequential chain where the output of one step is passed as input to the next step.
chain.invoke("India")