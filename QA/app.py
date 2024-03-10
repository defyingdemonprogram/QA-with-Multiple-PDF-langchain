import os
from typing import  Union, List

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Load environment variables securely
load_dotenv()

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# configure the page info
st.set_page_config(page_title="Multiple PDF Q/A App with Gemini", 
                   page_icon="👾")
st.title("Get Answer From Your PDF")


def get_pdf_text(pdf_paths: Union[List[str], str]) -> str:
    """Extracts text from multiple PDF files, handling potential exceptions."""
    texts = ""
    for pdf_path in pdf_paths:
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                texts += page.extract_text()
        except FileNotFoundError as ferr:
            print(f"[FileNotFoundError]: Pdf Path not found: {ferr}")
            st.error(f"File not found: {pdf_path}")
        except Exception as err:
            print(f"[Exception]: Error Processing the PDF: {err}")
            st.error(f"Error processing PDF: {err}")
    return texts

def get_text_chunks(text: str, chunk_size: int = 10_000, overlap: int = 1000) -> List[str]:
    """Splits text into manageable chunks with overlaps for context."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                   chunk_overlap=overlap)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks: List[str],
                     embedding_model: str="models/embedding-001"):
    """Creates a vector store from text chunks using the specified embedding model."""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
    except Exception as err:
        print("Error with Vector Store: ", err)
        st.error(f"[ERROR]: Vector Store Error: {err}")
    return vector_store


def get_conversational_chain():
    """Defines the prompt template and loads the conversational chain."""

    prompt_template = """
    Answer the question as detailed as possible. If the answer is not available in the context, \
        respond with "Answer not available in the context" and do not provide a random answer.

    Context: {context}
    Question: {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt, verbose=True)
    return chain

def answer_user_input(user_question, vector_store):
    """Processes user input, generates answer using the chain, and displays it."""

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    docs = vector_store.similarity_search(user_question, embeddings=embeddings)
    chain = get_conversational_chain()
    # get response from model
    response = chain.invoke({"input_documents": docs, "question": user_question})
    with st.chat_message("assistant"):
        st.write(response["output_text"])

    
def main():
    """Sets up Streamlit UI and processes user interaction."""

    # st.header("Chat with Multiple PDFs using Gemini")

    with st.sidebar:
        # Upload and process PDFs
        uploaded_pdfs = st.file_uploader("Upload PDF Files",
                                        type="pdf",
                                        accept_multiple_files=True)
    processed_text = None
    vector_store = None

    if uploaded_pdfs:
        with st.spinner("Processing PDFs..."):
            processed_text = get_pdf_text(uploaded_pdfs)
            with open("test.txt", "w") as fp:
                fp.write(processed_text)
            # get the processed text after splitting
            text_chunks = get_text_chunks(processed_text)
            # convert the text chunk in embeddings and store it
            vector_store = get_vector_store(text_chunks)
            st.success("Done processing PDFs.")

    # Handle user input
    # user_question = st.text_input("Ask a question about the PDFs:")
    if processed_text and vector_store:
        user_question = st.text_input("Ask a question about the PDFs:", "What is this PDF about?")
        if user_question:
          answer_user_input(user_question, vector_store)


if __name__=="__main__":
    main()