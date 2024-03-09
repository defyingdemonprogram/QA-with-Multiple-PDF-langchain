```python
import os
from typing import  Union, List

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

load_dotenv()
```
 ## PyPDF2
[Documentation](https://pypdf2.readthedocs.io/en/3.0.0/)

PyPDF2 is a pure-Python library capable of performing operations such as splitting, merging, cropping, and transforming the pages of PDF files. It can also retrieve text and metadata from PDF files. The `PdfReader` class is used to read the PDF file.

```python
from PyPDF2 import PdfReader

try:
    reader = PdfReader("my_example.pdf")

    # Extract metadata information about the PDF
    meta = reader.metadata
    print("Total pages in the PDF: ", len(reader.pages))

    # Extract text from the PDF
    text = ""

    for page in reader.pages:
        text += page.extract_text()
except Exception as exc:
    print(f"Error: {exc}")
```

**Note**: It must have seek attribute in `byte` object for PdfReader to load the pdf.
## LangChain
### Text Splitter
[Documentation](https://python.langchain.com/docs/modules/data_connection/document_transformers/recursive_text_splitter)
			
When dealing with larger documents, it's often necessary to split a long document into smaller chunks that fit within the model's context window. During this process, we aim to keep semantically related pieces of text together with some overlap.

The `RecursiveCharacterTextSplitter` is the recommended text splitter for generic text. It is parameterized by characters, with the split being done by a list of characters, and the chunk size measured by the number of characters. The default list includes `["\n\n", "\n", " ", ""]`. This default setting tries to keep all paragraphs, sentences, and words together as much as possible, as these are considered the strongest semantically related pieces of text.
	
### Google_genai
`GoogleGenerativeAIEmbeddings` optionally supports the `task_type`, which must be one of the following: `task_type_unspecified`, `retrieval_query`, `retrieval_document`, `semantic_similarity`, `classification`, or `clustering`.

```python
doc_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", task_type="retrieval_document"
)

# All of these will be embedded with the ‘retrieval_query’ task set
query_vecs = [query_embeddings.embed_query(q) for q in [query, query_2, answer_1]]
```

In retrieval, relative distance matters.