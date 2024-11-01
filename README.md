# Bayani - Document Chatbot

Bayani is a multilingual (English and Hausa) document question-answering application built with Streamlit and LangChain. It allows users to upload documents and ask questions about their content in multiple languages.

## Features

- Document upload and processing (PDF support)
- Multilingual interface (English and Hausa)
- Interactive chat interface
- Source reference for answers

## Prerequisites

- Python 3.11+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/ufakz/bayani](https://github.com/ufakz/bayani)
cd bayani
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Select your preferred language from the sidebar
3. Upload your PDF documents
4. Click "Process Documents" to analyze them
5. Start asking questions about your documents in the chat interface

## Dependencies

- streamlit
- langchain
- langchain-openai
- langchain-core
- PyPDF2
- python-dotenv