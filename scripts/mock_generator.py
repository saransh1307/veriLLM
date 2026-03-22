import json
import sys
import os

# this is mock generator for locally run the model
# Add root directory to python path for testing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import SalesforceDataPipeline

def generate_mock_salesforce_data():
    return [
        {
            "Id": "5003000000D8xyzAAA",
            "Subject": "Billing Issue",
            "Description": "Customer Michael Jordan called. His phone number is 312-555-0199 and his email is mjordan@bulls.com. He needs a refund sent to 1900 W Madison St, Chicago, IL 60612.",
            "Case_Comment__c": "Verified SSN is 000-11-2345 before processing the refund."
        },
        {
            "Id": "5003000000D8abcAAA",
            "Subject": "Login Help",
            "Description": "User Sarah Connor (s.connor@sky.net) is locked out. Re-routed to tech support at 800-555-9999.",
            "Case_Comment__c": "Sent password reset to s.connor@sky.net"
        }
    ]

def run_test():
    print("=====================================================")
    print("--- Starting veriLLM Mock Data Pipeline E2E Test ---")
    print("=====================================================\n")
    
    mock_data = generate_mock_salesforce_data()
    
    print("[!] Extracting Original Production Data...")
    
    # Initialize the core pipeline
    try:
        pipeline = SalesforceDataPipeline()
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize pipeline: {e}")
        return

    # Fields that typically contain unstructured text in Salesforce
    fields_to_clean = ["Description", "Case_Comment__c"]
    
    print("\n[*] Processing data through Local LLM Anonymization Engine...")
    print("    (Note: This requires Ollama running with Llama3 pulled)\n")
    
    try:
        # Run the sanitization process
        sanitized_data = pipeline.process_records(mock_data, fields_to_clean)
        
        print("\n[+] Verification Review (Original vs. Masked):")
        for i, record in enumerate(sanitized_data):
            print(f"\n--- Record {i+1} ---")
            orig_record = mock_data[i]
            for field in fields_to_clean:
                if field in record and field in orig_record:
                    print(f"[{field} - ORIGINAL]:\n{orig_record[field]}")
                    print(f"[{field} - MASKED]:\n{record[field]}\n")
        
        print("--- Test Complete ---")
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed during execution: {e}")
        print("Ensure 'ollama run llama3' has been executed locally or via the docker container.")

if __name__ == "__main__":
    run_test()
