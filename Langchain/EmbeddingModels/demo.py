from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-small" , 
                   dimensions=32     )

resukt = embedding.embed_query("What is the capital of France?")
print(resukt.content)


# getting mutiple embeddings at once 

documents = ["What is the capital of France?" ,
              "What is the capital of Germany?",
                "What is the capital of Italy?"
                "What is the capital of Spain?"
              ]

resukt = embedding.embed_documents(documents)
print(str(resukt.content ))