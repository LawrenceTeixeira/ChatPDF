import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from prettytable import PrettyTable
from pymongo import MongoClient
from dotenv import load_dotenv

# Load the variables from .env
load_dotenv(".env")

# OpenAI API Key and settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

## MongoDB vector database settings
# initialize MongoDB python client
MONGODB_ATLAS_CLUSTER_URI =  os.getenv("MONGODB_ATLAS_CLUSTER_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME =  os.getenv("COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME =  os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")

def LoadPDF():
  # Set up the RecursiveCharacterTextSplitter
  text_splitter = RecursiveCharacterTextSplitter(
      # Set a really small chunk size, just to show.
      chunk_size = 2000,
      chunk_overlap  = 0,
      length_function = len,
  )

  client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
  MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

  embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, chunk_size=2000)

  #Import PDF Loader and load the file
  loader = PyPDFDirectoryLoader("pdfs")

  file_content = loader.load()

  book_texts = text_splitter.split_documents(file_content)
  
  ## Save the documents to MongoDB Atlas
  book_docsearch = MongoDBAtlasVectorSearch.from_documents(
    documents=book_texts,
    embedding=embeddings,
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
  )
  
  return book_docsearch

def Query(query, book_docsearch, option):
  # Let's set up the query
  docs = book_docsearch.similarity_search(query)

  #docs = book_docsearch.max_marginal_relevance_search(query, k=5, fetch_k=10)

  # set up the llm model for our qa session
  if option == "text-davinci-003":
     llm = OpenAI(temperature=1, openai_api_key=OPENAI_API_KEY, model=option ) 
  else :
     llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=1, model_name=option )
  
  # Run the QA chain with your query to get the answer
  chain = load_qa_chain(llm, chain_type="stuff")
  
  # Initialize pretty table with column names
  table = PrettyTable(['Page', 'Source'])
  
  seen = set()
  
  rmanual = ""

  for doc in docs:
    page_content = doc.page_content
    page = doc.metadata.get('page', 'N/A')  # Default to 'N/A' if 'page' is not available
    source = doc.metadata.get('source', 'N/A')  # Default to 'N/A' if 'source' is not available
    
    if page != 'N/A':
       # check if the page and source combination is unique
       if (page, source) not in seen:

           if source == "pdfs\ManualdePatentes20210706.pdf":
              rmanual = rmanual + f", [Patents's manual (Page:"+str(page)+")](https://lawrence.eti.br/wp-content/uploads/2023/07/ManualdePatentes20210706-1.pdf)" 
           
           elif source == "pdfs\Manual_de_Marcas_3ª_edicao_6ª_revisao.pdf":
                rmanual = rmanual + f", [Tradmarks's manual (Page:"+str(page)+")](https://lawrence.eti.br/wp-content/uploads/2023/07/Manual_de_Marcas_3a_edicao_6a_revisao.pdf)" 

           elif source == "pdfs\Manual_de_DI_1a_edicao_1a_revisao.pdf":
                rmanual = rmanual + f", [Industrial Designs's manual (Page:"+str(page)+")](https://lawrence.eti.br/wp-content/uploads/2023/07/Manual_de_DI_1a_edicao_1a_revisao.pdf)" 

           elif source == "pdfs\modalidadecontratos.pdf":
                rmanual = rmanual + f", [Technology Contracts's manual (Page:"+str(page)+")](https://lawrence.eti.br/wp-content/uploads/2023/07/modalidadecontratos.pdf)" 
            
           elif source == "pdfs\Manual_de_IG_1a_edicao_2a_revisao.pdf":
                rmanual = rmanual + f", [Geographical Indications's manual (Page:"+str(page)+")](https://lawrence.eti.br/wp-content/uploads/2023/07/Manual_de_IG_1a_edicao_2a_revisao.pdf)" 
              
           elif source == "pdfs\manual-e-software-2022.pdf":
                rmanual = rmanual + f", [Computer Programs's manual (Page:"+str(page)+")](https://lawrence.eti.br/wp-content/uploads/2023/07/manual-e-software-2022.pdf)" 
            
           elif source == "pdfs\ManualdoUsurioeChipportugusV1.2.1.pdf":
                rmanual = rmanual + f", [Circuit Topographies's manual (Page:"+str(page)+")](https://lawrence.eti.br/wp-content/uploads/2023/07/ManualdoUsurioeChipportugusV1.2.1.pdf)" 
              
           elif source == "pdfs\manualcontratos.pdf":
                rmanual = rmanual + f", [Technology Contracts's manual (Page:"+str(page)+")](https://lawrence.eti.br/wp-content/uploads/2023/07/manualcontratos.pdf)" 
         
           table.add_row([page, source])
           seen.add((page, source))  # Add the combination to the set of seen combinations
      
  retorno = chain.run(input_documents=docs, question=query )

  print("Question: ", query)
  print("Answer: ", retorno + " Source: " + rmanual.replace(", ", "", 1) + '.')
  print (table)

  return retorno + " Source: " + rmanual.replace(", ", "", 1) + '.'

def LoadIndex():
  
  embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, chunk_size=2000)

  # book_docsearch = Pinecone.from_texts([t.page_content for t in book_texts], embeddings, index_name = index_name)
  book_docsearch = MongoDBAtlasVectorSearch.from_connection_string(
      MONGODB_ATLAS_CLUSTER_URI,
      DB_NAME + "." + COLLECTION_NAME,
      embeddings,
      index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
  )
    
  return book_docsearch