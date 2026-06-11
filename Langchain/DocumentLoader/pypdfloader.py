# this pypdfloader  make document loader for pdf files using pypdf library
# for exmple if we have 25 pdf then we will have 25 documents in the end and we can use these documents for further processing like text extraction, summarization, etc.
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("example.pdf")
docs = loader.load()
# this will give list docs dpeend on the pages we have 
# for example if we have 10 pages in the pdf then we will have 10 documents in the list docs

