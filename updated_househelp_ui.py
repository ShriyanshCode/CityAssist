import streamlit as st
import json
import requests
from datetime import date

def verify_nuid(nuid):
    url = "http://127.0.0.1:5000/verify_nuid"
    response = requests.post(url, json={"nuid": nuid})
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error during verification"}

def verify_aadhar(name, aadhaar_number, aadhaar_image_file):
    url = "http://127.0.0.1:5001/verify_aadhar"
    files = {"image": ("aadhaar_image.jpg", aadhaar_image_file, aadhaar_image_file.type)}
    data = {"name": name, "aadhaar_number": aadhaar_number}
    response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error during Aadhaar verification"}

def add_to_json(data):
    try:
        with open('data/data2.json', 'r') as f:
            househelps = json.load(f)
    except FileNotFoundError:
        househelps = []

    househelps.append(data)

    with open('data/data.json', 'w') as f:
        json.dump(househelps, f, indent=4)

# Streamlit app 
st.title("House Help Details")

with st.form("househelp_form"):
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    job_title = st.text_input("Job Title")
    number = st.text_input("Phone Number")
    timework = st.text_input("Time Worked (in years)")
    desc = st.text_area("Description")
    
    nuid = st.text_input("Enter NUID (Nursing ID) if nurse")
    aadhaar_name = st.text_input("Enter Name as per Aadhaar")
    aadhaar_number = st.text_input("Enter Aadhaar Number")
    aadhaar_image = st.file_uploader("Upload Aadhaar Image", type=["jpg", "jpeg", "png"])

    submit_button = st.form_submit_button("Submit")

if submit_button:
    age = (date.today() - dob).days // 365
    
    aadhaar_verification_status = "NULL"

    # Aadhaar Verification
    if aadhaar_name and aadhaar_number and aadhaar_image:
        with st.spinner('Validating Aadhaar...'):
            aadhar_verification_result = verify_aadhar(aadhaar_name, aadhaar_number, aadhaar_image)
            if "error" in aadhar_verification_result:
                st.warning("Error during Aadhaar verification.")
            else:
                if aadhar_verification_result.get("verification") == "Verified":
                    st.success("Aadhaar verified successfully.")
                    aadhaar_verification_status = "verified"
                else:
                    st.warning("Aadhaar verification failed.")

    # NUID Verification
    nuid_verification_result = None
    if nuid:
        with st.spinner('Validating NUID...'):
            verification_result = verify_nuid(nuid)
            if "error" in verification_result:
                st.warning("Error during NUID verification.")
            else:
                if verification_result.get("verification") == "Verified":
                    nuid_verification_result = nuid
                    st.success("NUID verified and added.")
                else:
                    nuid_verification_result = "not verified"
                    st.warning("NUID could not be verified.")

    househelp_data = {
        "name": name,
        "dob": str(dob),
        "age": age,
        "gender": gender,
        "job_title": job_title,
        "number": number,
        "timework": timework,
        "nuid": "NULL" if not nuid_verification_result else nuid_verification_result,
        "aadhaar": aadhaar_verification_status,
        "desc": desc
    }

    add_to_json(househelp_data)
    st.success("House help details added successfully!")
