import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")


def ask_llm(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            return response.text
        except errors.ServerError:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)  # wait 1s, then 2s, then give up


if __name__ == "__main__":
    print(ask_llm("Say hello in one short sentence."))