# this is for the parellel chain example, we will be using two different models to generate a summary and a quiz about a given topic, and then merge the results into a single output.

from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablepParellel
# use for excuting multiple chains in parallel and then merging the results.


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.9)
model2 = ChatAnthropic(model="claude-2", temperature=0.9)
parser = StrOutputParser()

prompt1 = PromptTemplate(
    template = "generate a short note from the folllowing {Topic}?"
    input_variables = ["Topic"]
)


prompt2= PromptTemplate(
    template = "Desgin a short 5 question quiz about {text}?"
    input_variables = ["text"]
)


prompt2= PromptTemplate(
    template = "merge the question and topics summary into single {topics} and {questions}?"
    input_variables = ["topics", "questions"]

)


parellel_chain = RunnablepParellel({ 
    'notes' : prompt1 | model1 | parser,
    'quiz' : prompt2  | model2 | parser
})

merge_chain = prompt3 | model1 | parser

chain = parellel_chain | merge_chain
res = chain.invoke("India")
print(res)

