# Career Advisor
Welcome to Career Advisor, a RAG application that provides personalized career advice based on uploaded documents such as resumes, cover letters, and job postings.

## How to Use
1. **Upload Documents**: Click the file uploader and select one or more documents (.pdf, .txt, .md)
2. **Wait for Processing**: The application will chunk and index your documents
3. **Ask Questions**: Type questions like:
   - "What skills should I develop for a data science role?"
   - "How does my experience match this job posting?"
   - "What are my strongest qualifications?"
4. **Get Advice**: Receive personalized, actionable career guidance


## Changes to Provided Configuration
1. Changed the names of the files:
   - career_advisor.py: full app that combines langchain and streamlit
   - langchain_code.ipynb: Jupiternotebook used to test the langchain code, based on the class template
   - streamlit_code.py: python file used to test the streamlit code, based on the class template
2. Deleted the data txt and uploaded Resume Maria Chang.pdf for tests.
3. Added pdfpumlber to the requirement text
4. Updated to langchain-chroma==1.00
5. Changed the system prompt and messages so that it adapts from just a pdf uploader to a career advisor. 
6. changed the code so that it now uploads txt, pdf, and md. 
7. changed the code so that it now allows multiple uploads. 

## Implementation Details
- Chunk size: 500 tokens with 50-token overlap
- Retrieval: Top 5 most relevant chunks per query
- Embedding model: OpenAI text-embedding-3-large
- Vector store: ChromaDB

## To Run the Application

Set your API key and start the application:
```bash
API_KEY="your_actual_API_KEY" streamlit run career_advisor.py
```

Or set the key separately:
```bash
export API_KEY="your_actual_API_KEY"
streamlit run career_advisor.py
```
