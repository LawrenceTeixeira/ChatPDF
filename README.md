# Procedures of the Brazilian Patent and Trademark Office (BRPTO) Chatbot

## Overview
This repository contains the code for a Streamlit-based chatbot that provides guidance on the fundamental procedures of the Brazilian Patent and Trademark Office (BRPTO). It covers various aspects such as trademarks, patents, industrial designs, geographical indications, computer programs, circuit topographies, and technology contracts.

## Features
- Interactive chat interface to query BRPTO's official manuals.
- Integration with various GPT models for accurate and relevant responses.
- Direct links to official BRPTO manuals and resources.
- MongoDB Atlas for document storage and retrieval.

## Installation
1. Clone the repository:

```bash
git clone https://github.com/LawrenceTeixeira/ChatPDF.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run bot.py
```

4. Complete the .env.example with your information and rename to .env file.
```bash
OPENAI_API_KEY=your_openai_api_key
MONGODB_USER=your_mongodb_user
MONGODB_PASSWORD=your_mongodb_password
MONGODB_CLUSTER=your_mongodb_cluster
DB_NAME=your_database_name
COLLECTION_NAME=your_collection_name
ATLAS_VECTOR_SEARCH_INDEX_NAME=your_atlas_vector_search_index_name
```

## Author
- [Lawrence Teixeira](https://www.linkedin.com/in/lawrenceteixeira/) - Creator and Developer
- Blog: [Lawrence's Blog](https://lawrence.eti.br) - Follow my blog for more projects and updates.

## Usage
After starting the application, use the chat interface to ask questions related to BRPTO's procedures. The chatbot will respond with relevant information extracted from the official manuals.

## Contributing
Contributions to this project are welcome. Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- Brazilian Patent and Trademark Office (BRPTO)
- Lawrence Teixeira for creating the project
- OpenAI for GPT models

## Disclaimer
Please note that this chatbot has no affiliation with the Brazilian Patent and Trademark Office (BRPTO).
