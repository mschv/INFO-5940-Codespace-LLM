## Reference Log

### 1. Log all the external sources and tools used in this assignment
For this assigment I have use:
- Claude Code for debugging
- Claude to improve my system prompt
- Databricks community to read about chunking best practices: https://community.databricks.com/t5/technical-blog/the-ultimate-guide-to-chunking-strategies-for-rag-applications/ba-p/113089
- Streamlit forum to read how to upload multiple pdf files in streamlit: https://discuss.streamlit.io/t/how-to-upload-a-pdf-file-in-streamlit/2428/2

### 2.Document any GenAI usage with a brief rationale explaining how it was used and why
- I used Claude to improve my system prompt and the messages to make my app easier to understand by users.
- I used ClaudeCode to debug my code:
    - The class examples had separate implementations of langchain and streamlit. When I tried to integrate the code in just one .py file, I had issues to make it work all together. I asked Claude to tell me why it wasn't working and it helped me to identify the proper sequence and state management approach.
    - When I added the multiple pdf files function that I got from the forum, it wasn't working properly. Claude helped debug why files weren't being processed in the loop and fixed the document creation logic.
    - I had issues to hide my API key, I asked Claude for help and it suggested me to use os.getenv()