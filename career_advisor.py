import streamlit as st
import os
import pdfplumber
import chardet
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

#FUNCTIONS
# Read text file
def read_text_file(raw_data):
    detected = chardet.detect(raw_data)
    encoding = detected['encoding'] or 'utf-8'
    
    try:
        return raw_data.decode(encoding)
    except:
        return raw_data.decode('utf-8', errors='ignore')


# Extract data from pdf or text file
def extract_file_content(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        with pdfplumber.open(uploaded_file) as pdf:
            return "".join(page.extract_text() for page in pdf.pages)
    else:
        raw_data = uploaded_file.read()
        return read_text_file(raw_data)


# Create documents from uploaded files
def create_documents(uploaded_files):
    documents = []
    for uploaded_file in uploaded_files:
        content = extract_file_content(uploaded_file)
        doc = Document(
            page_content=content,
            metadata={"source": uploaded_file.name}
        )
        documents.append(doc)
    return documents


# Split documents into chunks
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_documents(documents)


#create vector store to store chunks
def create_vectorstore(chunks):
   vectorstore = Chroma.from_documents(
       documents=chunks,
       embedding=OpenAIEmbeddings(model="openai.text-embedding-3-large")
       )
   return vectorstore


# Format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#SETUP MODEL AND KEYS
llm = ChatOpenAI(
   model="openai.gpt-4o",
   temperature=0.2,
   openai_api_key=os.getenv('API_KEY'),
   openai_api_base=os.getenv('OPENAI_BASE_URL')
)

#UI
st.title("💼 Career advisor")
uploaded_files = st.file_uploader(
   "📄 Upload your documents: resume, cover letter, job postings, or anything relevant to your career goals.",
   type=['pdf', 'txt', 'md'],
   accept_multiple_files=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I'm here to help. Upload your documents above, then tell me what you're working towards!"}]

if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = None

if "documents_loaded" not in st.session_state:
    st.session_state["documents_loaded"] = False

# PROCESS UPLOADED FILES
if uploaded_files and not st.session_state["documents_loaded"]:
    st.write("📄 Processing documents...")
    
    with st.spinner("Storing.."):
        # Create documents
        documents = create_documents(uploaded_files)
        print(f"Documents created: {len(documents)}")  # Debug
        
        # Split documents
        chunks = split_documents(documents)

        # Create vector store
        st.session_state["vectorstore"] = create_vectorstore(chunks)
        st.session_state["documents_loaded"] = True
        st.success("✅ Documents processed successfully!")

# DISPLAY CHAT HISTORY
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# QUESTION INPUT & PROCESSING
question = st.chat_input(
    "Write a question",
    disabled=st.session_state["vectorstore"] is None,
)

if question and st.session_state["vectorstore"]:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # 1. Retrieve relevant documents
            vectorstore = st.session_state["vectorstore"]
            retrieved_docs = vectorstore.similarity_search(question, k=5)
            
            # 2. Format context
            context = format_docs(retrieved_docs)
            
            # 3. Create prompt for career analysis
            system_instructions = (
                "You are an experienced career advisor. Your role is to provide personalized career guidance based on the documents provided to you.\n"
                "Use the provided context and analyze the information to provide actionable advice to help the person achieve their objectives. Focus on being specific, practical, and encouraging in your recommendations\n"
                "Base your advice solely on the information provided in the documents. If important information is missing, acknowledge this and work with what you have or ask clarifying questions.\n"
                "Keep your advice concise and focused. Prioritize the most important insights rather than being exhaustive. Aim for clarity and impact over comprehensiveness.\n"
                f"Context:\n{context}"
            )
            
            # 4. Get response from LLM
            response = llm.invoke([
                SystemMessage(content=system_instructions),
                HumanMessage(content=question),
            ])
            
            answer = response.content
            st.write(answer)
            
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})