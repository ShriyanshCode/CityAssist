import getpass
import os
import json

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.schema import Document

from pymongo import MongoClient
from params import MONGO_URI, GOOGLE_API_KEY

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
client = MongoClient(MONGO_URI)

dbName = "cityassist2"
collectionName = "househelp"
collection = client[dbName][collectionName]

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

dir_path = 'data'
all_documents = []

# Parse data
for file_name in os.listdir(dir_path):
    file_path = os.path.join(dir_path, file_name)
    
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            data = []
            
            for entry in json_data:
                document = {
                    "name": entry.get("name"),
                    "dob": entry.get("dob"),
                    "age": entry.get("age"),
                    "gender": entry.get("gender"),
                    "job_title": entry.get("job_title"),
                    "number": entry.get("number"),
                    "timework": entry.get("timework"),
                    "nuid": entry.get("nuid"),
                    "aadhaar": entry.get("aadhaar"),  
                    "desc": entry.get("desc")
                }
                data.append(document)

            documents = [
                Document(
                    page_content=(
                        f"Name: {doc['name']}\n"
                        f"Date of Birth: {doc['dob']}\n"
                        f"Age: {doc['age']}\n"
                        f"Gender: {doc['gender']}\n"
                        f"Job Title: {doc['job_title']}\n"
                        f"Phone Number: {doc.get('number', 'N/A')}\n"
                        f"Time Worked: {doc.get('timework', 'N/A')}\n"
                        f"NUID: {doc.get('nuid', 'N/A')}\n"
                        f"Aadhaar Status: {doc.get('aadhaar', 'N/A')}\n"  
                        f"Description: {doc['desc']}"
                    ),
                    metadata={**doc}
                ) for doc in data
            ]
            
            all_documents.extend(documents) 
            collection.insert_many(data)  #

# Vector store setup
vectorStore = MongoDBAtlasVectorSearch.from_documents(
    all_documents,
    embeddings,
    collection=collection
)

print("Documents have been successfully processed and stored in MongoDB.")
