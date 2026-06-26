import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

def main():
    # Load environment variables from .env
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"Loaded GEMINI_API_KEY: {api_key}")
    
    if not api_key or api_key == "YOUR_API_KEY":
        print("\n[!] Warning: GEMINI_API_KEY is not set or is using the placeholder 'YOUR_API_KEY'.")
        print("Please replace YOUR_API_KEY in the .env file with your actual Gemini API Key from Google AI Studio.")
        print("\nChecking if we can fall back to Vertex AI using your Google Cloud credentials...")
        
        # Try Vertex AI using Application Default Credentials
        try:
            print("Attempting to initialize Gemini Client in Vertex AI mode...")
            # Using the authenticated project 920825116361 and standard region
            client = genai.Client(vertexai=True, project="920825116361", location="us-central1")
            
            print("Sending a test prompt to gemini-2.5-flash via Vertex AI...")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents='Hello! Please reply with a short greeting confirming you can hear me.',
            )
            print("\n[+] Success! Response from Gemini via Vertex AI:")
            print(f"-> {response.text.strip()}\n")
            return
        except Exception as e:
            print(f"[-] Vertex AI fallback failed: {e}")
            print("\nPlease set a valid GEMINI_API_KEY in the .env file and run again.")
            sys.exit(1)

    # Initialize client with the API key from environment
    try:
        print("Initializing Gemini Client using GEMINI_API_KEY...")
        client = genai.Client()
        
        print("Sending a test prompt to gemini-2.5-flash...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Hello! Please reply with a short greeting confirming you can hear me.',
        )
        print("\n[+] Success! Response from Gemini:")
        print(f"-> {response.text.strip()}\n")
    except APIError as e:
        print(f"\n[-] API Error: {e}")
        print("This is likely due to an invalid or inactive API key. Please check your GEMINI_API_KEY in the .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[-] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
