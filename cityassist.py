import streamlit as st
import os
from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from params import MONGO_URI, GOOGLE_API_KEY

client = MongoClient(MONGO_URI)
dbName = "cityassist2"
collectionName = "househelp2"
collection = client[dbName][collectionName]

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorStore = MongoDBAtlasVectorSearch(collection, embeddings)

def query_data(query, k=5):
    docs = vectorStore.similarity_search(query, k=k)
    if not docs:
        return None

    try:
        raw_contents = [doc.page_content for doc in docs]
        return raw_contents
    except Exception as e:
        return None

# Streamlit UI
st.title("City Assist - House Help Finder")

query = st.text_input("What househelp do you need?")
search_button = st.button("Search")  
if search_button and query:  
    with st.spinner("Searching for the best matches..."):
        as_outputs = query_data(query)

        if as_outputs is None:
            st.write("No results found.")
        else:
            st.subheader("Top 5 Similar Matches:")
            
            for i, output in enumerate(as_outputs, 1):
                with st.container():
                    st.markdown(
                        f"""
                        <div style="background-color: #f0f0f5; padding: 20px; border-radius: 10px; margin: 10px 0;">
                            <h4 style="color: #800080;">Match {i}</h4>
                            <p style="color: #0000FF;">{output if output else "No content available"}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
