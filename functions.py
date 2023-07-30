import openai, langchain, pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader
from langchain.document_loaders import PyPDFDirectoryLoader
from prettytable import PrettyTable

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
 # loader = PyPDFLoader("https://lawrence.eti.br/wp-content/uploads/2023/07/ManualdePatentes20210706.pdf")
  loader = PyPDFDirectoryLoader("pdfs")

  file_content = loader.load()

  book_texts = text_splitter.split_documents(file_content)

  if index_name not in pinecone.list_indexes():
      print("Index does not exist: ", index_name)

  book_docsearch = Pinecone.from_documents(book_texts, embeddings, index_name = index_name)

  return book_docsearch

def Query(query, book_docsearch, option):
  # Let's set up the query
  docs = book_docsearch.similarity_search(query)

  #docs = book_docsearch.max_marginal_relevance_search(query, k=5, fetch_k=10)

  # set up the llm model for our qa session
  if option == "text-davinci-003":
     llm = OpenAI(temperature=1, openai_api_key=OPENAI_API_KEY, model=option ) 
  else :
     llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model_name=option )
  
  # Run the QA chain with your query to get the answer
  chain = load_qa_chain(llm,   chain_type="stuff")
  
  print(docs)

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
              rmanual = rmanual + f", [Patents's manual](https://lawrence.eti.br/wp-content/uploads/2023/07/ManualdePatentes20210706-1.pdf)" 
           
           elif source == "pdfs\Manual_de_Marcas_3ª_edicao_6ª_revisao.pdf":
                rmanual = rmanual + f", [Tradmarks's manual](https://lawrence.eti.br/wp-content/uploads/2023/07/Manual_de_Marcas_3a_edicao_6a_revisao.pdf)" 

           elif source == "pdfs\GuiadoUsurioDI.pdf":
                rmanual = rmanual + f", [Industrial Designs's manual](https://lawrence.eti.br/wp-content/uploads/2023/07/GuiadoUsurioDI.pdf)" 

           elif source == "pdfs\Manual_de_IG_1a_edicao_2a_revisao.pdf":
                rmanual = rmanual + f", [Geographical Indications's manual](https://lawrence.eti.br/wp-content/uploads/2023/07/Manual_de_IG_1a_edicao_2a_revisao.pdf)" 
              
           elif source == "pdfs\manual-e-software-2022.pdf":
                rmanual = rmanual + f", [Computer Programs's manual](https://lawrence.eti.br/wp-content/uploads/2023/07/manual-e-software-2022.pdf)" 
            
           elif source == "pdfs\ManualdoUsurioeChipportugusV1.2.1.pdf":
                rmanual = rmanual + f", [Circuit Topographies's manual](https://lawrence.eti.br/wp-content/uploads/2023/07/ManualdoUsurioeChipportugusV1.2.1.pdf)" 
              
           elif source == "pdfs\manualcontratos.pdf":
                rmanual = rmanual + f", [Technology Contracts's manual](https://lawrence.eti.br/wp-content/uploads/2023/07/manualcontratos.pdf)" 
         
           table.add_row([page, source])
           seen.add((page, source))  # Add the combination to the set of seen combinations
      
  print (table)

  retorno = chain.run(input_documents=docs, question=query )

  return retorno + " Source: " + rmanual.replace(", ", "", 1) + '.'

def LoadIndex():
  # Set the index name for this project in pinecone first 
  # Pinecone related setup
  pinecone.init(
          api_key = PINECONE_API_KEY,
          environment = PINECONE_ENV
  )
  
  embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, chunk_size=2000)

  # book_docsearch = Pinecone.from_texts([t.page_content for t in book_texts], embeddings, index_name = index_name)
  book_docsearch = Pinecone.from_existing_index("pine-search", embeddings )

  return book_docsearch