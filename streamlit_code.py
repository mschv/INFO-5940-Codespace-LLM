import streamlit as st
import os
import pdfplumber
import chardet
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url="https://api.ai.it.cornell.edu",
)

st.title("💼 Career advisor")
uploaded_files = st.file_uploader(
    "📄 Upload your documents: resume, cover letter, job postings, or anything relevant to your career goals.", 
    type=['pdf', 'txt', 'md'],
    accept_multiple_files=True
)

question = st.chat_input(
    "Hi! I'm here to help. Upload your documents above, then tell me what you're working towards!",
    disabled=not uploaded_files,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I'm here to help. Upload your documents above, then tell me what you're working towards!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question and uploaded_files:
    all_content = ""  # Combine content from all uploaded files
    
    # Read the content based on file type
    for uploaded_file in uploaded_files:  # Loop through each file
        st.write(f"📄 Processing documents: {uploaded_file.name}")
        
        if uploaded_file.name.endswith('.pdf'):
            with pdfplumber.open(uploaded_file) as pdf:
                file_content = "".join(page.extract_text() for page in pdf.pages)
        else:
            # Handle TXT and MD files
            raw_data = uploaded_file.read()
            detected = chardet.detect(raw_data)
            encoding = detected['encoding'] or 'utf-8'
            
            try:
                file_content = raw_data.decode(encoding)
            except:
                file_content = raw_data.decode('utf-8', errors='ignore')
        
        all_content += f"\n\n--- File: {uploaded_file.name} ---\n{file_content}"
    
    print(f"Total content length: {len(all_content)}")

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Here's the content of the files:\n\n{all_content}"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})