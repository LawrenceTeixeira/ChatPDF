import openai, langchain, pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader

# OpenAI API Key and settings
OPENAI_API_KEY = "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"
embed_model = "text-embedding-ada-002"

## Pinecone vector database settings
PINECONE_API_KEY = "fe78818e-e21b-4b49-aae8-c9d1ecde475b"
PINECONE_ENV = "us-west4-gcp-free"

def LoadPDF():
  # Set up the RecursiveCharacterTextSplitter
  text_splitter = RecursiveCharacterTextSplitter(
      # Set a really small chunk size, just to show.
      chunk_size = 2000,
      chunk_overlap  = 0,
      length_function = len,
  )

  # Pinecone related setup
  pinecone.init(
          api_key = PINECONE_API_KEY,
          environment = PINECONE_ENV
  )

  # Set the index name for this project in pinecone first
  index_name = 'pine-search'
 
  embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, chunk_size=2000)

  #Import PDF Loader and load the file
  loader = PyPDFLoader("https://lawrence.eti.br/wp-content/uploads/2023/07/ManualdePatentes20210706.pdf")

  file_content = loader.load()

  book_texts = text_splitter.split_documents(file_content)

  if index_name not in pinecone.list_indexes():
      print("Index does not exist: ", index_name)

  book_docsearch = Pinecone.from_texts([t.page_content for t in book_texts], embeddings, index_name = index_name)

  return book_docsearch

def Query(query, book_docsearch):
  # Let's set up the query
  docs = book_docsearch.similarity_search(query)

  # set up the llm model for our qa session
  llm = OpenAI(temperature=1, openai_api_key=OPENAI_API_KEY, model="text-davinci-003"  ) 
  
  # Run the QA chain with your query to get the answer
  chain = load_qa_chain(llm, chain_type="stuff")
  
  retorno = chain.run(input_documents=docs, question=query)

  return retorno

