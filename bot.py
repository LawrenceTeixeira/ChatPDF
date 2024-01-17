import openai
import streamlit as st
from functions import LoadPDF, Query, LoadIndex

book_docsearch = LoadIndex()
#book_docsearch = LoadPDF()

st.set_page_config(
    page_title="Procedures of the Brazilian Patent and Trademark Office (BRPTO)",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.gov.br/inpi/pt-br',
        'About': "This app is designed to guide you through the fundamental procedures of safeguarding your trademarks, patents, industrial designs, geographical indications, computer programs, circuit topographies, and technology contracts with the Brazilian Patent and Trademark Office (BRPTO)."
    }
)
   
with st.sidebar:
    st.image("https://lawrence.eti.br/wp-content/uploads/2023/07/Untitled-300-×-100-px-1.png")   
    option = st.selectbox(
    'Which version of the GPT model do you prefer to use?',
    ('gpt-4-1106-preview', 'gpt-4', 'gpt-3.5-turbo' ),)
    ""
    "Official Manuals of the BRPTO:"
    "[Tradmarks](https://lawrence.eti.br/wp-content/uploads/2023/07/Manual_de_Marcas_3a_edicao_6a_revisao.pdf)"
    "[Patent](https://lawrence.eti.br/wp-content/uploads/2023/07/ManualdePatentes20210706-1.pdf)"
    "[Industrial Designs](https://lawrence.eti.br/wp-content/uploads/2023/07/Manual_de_DI_1a_edicao_1a_revisao.pdf)"
    "[Geographical Indications](https://lawrence.eti.br/wp-content/uploads/2023/07/Manual_de_IG_1a_edicao_2a_revisao.pdf)"
    "[Computer Programs](https://lawrence.eti.br/wp-content/uploads/2023/07/manual-e-software-2022.pdf)"
    "[Circuit Topographies](https://lawrence.eti.br/wp-content/uploads/2023/07/ManualdoUsurioeChipportugusV1.2.1.pdf)"
    "[Technology Contracts](https://lawrence.eti.br/wp-content/uploads/2023/07/manualcontratos.pdf)"
    ""
    "Source: [BRPTO](https://www-gov-br.translate.goog/inpi/pt-br?_x_tr_sl=pt&_x_tr_tl=en&_x_tr_hl=pt-BR&_x_tr_pto=wapp)"
    ""
    "Created by [Lawrence Teixeira](https://www.linkedin.com/in/lawrenceteixeira/)"
    ""
    ""
    "Please note that this chatbot has no affiliation with the Brazilian Patent and Trademark Office (BRPTO)."

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hey, 😊 how are you? Feel free to ask me questions in any language about the BRPTO's Official Manuals."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner('Searching...'): 
      response = Query(prompt, book_docsearch, option)
    
    if response:
        result = (str(response))
    else:
        result = (str(":)"))


    msg = { "role": "assistant",
            "content": result
    }

    st.session_state.messages.append(msg)
       
    st.chat_message("assistant").write(msg["content"])
