import json
import sys
import time
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/verify_nuid', methods=['POST'])
def verify_nuid():
    nuid = request.json.get('nuid')
    
    if not nuid:
        return jsonify({"error": "NUID is required"}), 400

    driver_path = r'C:\STUFF\Docs\sem5\aistuf\cityassist\chromedriver.exe'
    driver = webdriver.Chrome(service=Service(driver_path))

    driver.get("https://nrts.indiannursingcouncil.gov.in/login.nic")

    try:
        nuid_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="nuidvalue"]'))
        )
        nuid_input.send_keys(nuid)

        fetch_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="4div"]/div[2]/div[2]/input'))
        )
        fetch_button.click()

        status = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="nuid_status1"]/span'))
        ).text
        nuid_text = driver.find_element(By.XPATH, '//*[@id="appl_nuid"]').text
        nurse_name = driver.find_element(By.XPATH, '//*[@id="appl_name"]').text
        council = driver.find_element(By.XPATH, '//*[@id="councilname"]').text

        if status.lower() == "active" and nuid_text == nuid:
            result = {
                "verification": "Verified",
                "nuid": nuid_text,
                "name": nurse_name,
                "council": council,
                "status": status
            }
        else:
            result = {
                "verification": "Not Verified",
                "nuid": nuid_text,
                "name": nurse_name,
                "status": status
            }
        
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
