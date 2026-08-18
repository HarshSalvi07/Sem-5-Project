# main.py
import os
import sys
import json
from groq import Groq
from dotenv import load_dotenv

# Automatically locate and load variables from your local .env file
# Load variables from .env
load_dotenv()

# Add the project root to Python's import path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
sys.path.insert(0, PROJECT_ROOT)

from src.prompts import ANALYSIS_PROMPT

def run_automated_pipeline(json_path: str):
    print("NOTE: This process may take up to 30 seconds, please be patient")
    print("📄 Step 1: Loading raw JSON document...")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return

    # Convert the entire JSON into a clean string for the prompt
    extracted_text = json.dumps(data, indent=2, ensure_ascii=False)

    print("✅ JSON document loaded successfully!")

    print("📝 Step 2: Preparing consistent prompt structure...")
    final_prompt = ANALYSIS_PROMPT.format(data=extracted_text)

    print("🧠 Step 3: Routing text payload directly to openai/gpt-oss-120b...")
    try:
        client = Groq()

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict, rule-following Academic Advisor. Always adhere strictly to the requested markdown output format blocks without conversational intro or outro fluff."
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=2.0,
            max_tokens=2048,
            top_p=1.0,
            stream=False,
        )

        print("Thank you for waiting, we appreciate your patience")
        print("\n=========================================================== ✨ PERFORMANCE ANALYSIS REPORT =============================================================")
        print("")
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ LLM Automation Error: {str(e)}")


if __name__ == "__main__":
    # Change this to the name of your JSON file
    target_json_file = "raw_document.json"

    if os.path.exists(target_json_file):
        run_automated_pipeline(json_path=target_json_file)
    else:
        print(f"❌ File Error: Please save your JSON as '{target_json_file}' in this folder.")