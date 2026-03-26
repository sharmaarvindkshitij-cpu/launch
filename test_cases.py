import requests
import json
import time
import subprocess
import os
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("Testing FraudShield AI API...")
    
    test_cases = [
        # Scams
        {"type": "message", "content": "URGENT! Your account has been suspended. Click here to verify your identity.", "expected": "Fraud"},
        {"type": "message", "content": "Congratulations! You won $5000.", "expected": "Fraud"}, # Or Suspicious
        
        # Safe 
        {"type": "message", "content": "Hey, can we meet tomorrow at 10 AM for the project discussion?", "expected": "Safe"},
        
        # URLs
        {"type": "url", "content": "http://192.168.1.1/login.php", "expected": "Fraud"},
        {"type": "url", "content": "https://bit.ly/3xyzverify", "expected": "Suspicious"},
        {"type": "url", "content": "https://www.google.com", "expected": "Safe"},
        
        # UPI
        {"type": "upi", "content": "pmcares@sbi", "expected": "Fraud"},
        {"type": "upi", "content": "john.doe@okicici", "expected": "Safe"},
        {"type": "upi", "content": "customer.helpdesk@ybl", "expected": "Fraud"}
    ]
    
    for case in test_cases:
        try:
            res = requests.post(f"{BASE_URL}/analyze", json={"type": case["type"], "content": case["content"]})
            if res.status_code == 200:
                data = res.json()
                print(f"[TEST {case['type'].upper()}] Input: '{case['content']}'")
                
                if case['type'] == 'url':
                    print(f"Risk Score: {data.get('overall_assessment', {}).get('risk_score_numeric', 'N/A')}")
                    print(f"Classification: {data.get('overall_assessment', {}).get('risk_level', 'N/A')} (Expected: {case['expected']})")
                    print(f"Reasons: {data.get('final_explanation', 'N/A')}")
                else:
                    print(f"Risk Score: {data.get('risk_score')}")
                    print(f"Classification: {data.get('classification')} (Expected: {case['expected']})")
                    print(f"Reasons: {data.get('reasoning')}")
                    
                print("-" * 40)
            else:
                print(f"Error {res.status_code} on {case['content']}: {res.text}")
        except Exception as e:
            print(f"Failed to connect: {str(e)}")

if __name__ == "__main__":
    # Start the server in the background using the same python executable
    print("Starting Flask Server...")
    proc = subprocess.Popen([sys.executable, "app.py"], env=os.environ, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3) # Wait for server to start
    try:
        test_api()
        
        print("\nTesting History Endpoint:")
        res = requests.get(f"{BASE_URL}/history?limit=3")
        print("History Items Count:", len(res.json()))
        
    finally:
        print("Terminating Flask Server...")
        proc.terminate()
