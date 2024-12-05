# City Assist: Streamlined Platform for Household Help

City Assist is a web application designed to simplify the search for reliable household help by delivering the top 10 relevant matches based on user needs. The platform focuses on efficiency, verification, and user experience, using advanced techniques to ensure accurate and secure results.
## Current Working:
#### Top 5 similar search results  of the query “drivers in delhi”.
![image](https://github.com/user-attachments/assets/351e72cd-162c-4463-9e56-7668b2b436d3)
#### Aadhaar Verification along with Aadhar Card.
![image](https://github.com/user-attachments/assets/024bebfc-3d43-41e7-87fc-a65f7da8c1b9)
#### Nursing Verification using Selenium.
![image](https://github.com/user-attachments/assets/0ff46743-4f4e-4e14-8f52-aa81b2eb53ed)

Aadhar Card from: https://www.scribd.com/document/432565930/Adhar-card-sample 
## Methodology

### Identity Verification with Selenium
City Assist automates professional ID verification using Selenium for browser interactions, which verifies IDs on official portals. This helps ensure authenticity at scale, especially for specific professions such as nursing.

### Aadhaar Verification with PaddleOCR
The platform uses PaddleOCR for Aadhaar card verification. By extracting and matching text from Aadhaar images, City Assist validates user-provided details, enhancing security and reducing manual effort.

### Advanced Search with MongoDB Vector Search and Google Embeddings
City Assist employs vector-based search with MongoDB and Google Embeddings, enabling efficient and nuanced matching of user queries with household help profiles. This provides more accurate results compared to basic conditional filtering.

### Frontend Development with Streamlit
Streamlit provides a fast, responsive UI for City Assist, enabling users to quickly search, filter, and verify profiles with minimal lag, enhancing the overall experience.

## Implementation

City Assist combines vector search with MongoDB, OCR verification with PaddleOCR, and Selenium automation, creating a user-friendly platform for reliable and fast household help matching.

## Pre-Requisites:
An account on MongoDB, with network access as 0.0.0.0/0 (access anywhere) or any specific IP address.
and preferably a database access with a new user and password to your cluster (for Mongo URI).
1. Connect to mongodb cluster using, this is MONGO_URI:
  mongodb+srv://<user_id>:<user_password>@cluster0.ozbxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
2. Gemini API Key this is GOOGLE_API_KEY:
   Access it here: https://aistudio.google.com/app/apikey
3. Chromium driver
4. Edit MONGO_URI and GOOGLE_API_KEY 
## Running the Code
1. Necessary packages:
```bash
pip install -r requirements.txt
``` 
2. Load dataset in your own Mongo Database Cluster:
```bash
py load.py
```
3. Create a Atlas Search Index on Mongo DB, below is the index overview we have used as this has been made using Google Gemini embeddings and Gemini. You can copy paste this on JSON editor portion, after creating search index:
```bash
   {
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "dimensions": 768,
        "similarity": "cosine",
        "type": "knnVector"
      }
    }
  }
}
```
4. Run the flask server for Aadhaar Verification.
```bash
py aadhaarchecker.py
```
6. Run flask server for NUID Verification of nurses.
```bash
py nursechecker.py
```
8. Househelp Data Entry and Verification
```bash
streamlit run updated_househelp_ui.py
```
10. Househelp Search
```bash
streamlit run cityassist.py
```
