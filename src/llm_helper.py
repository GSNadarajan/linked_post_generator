from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

llm = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name="llama-3.2-90b-vision-preview"
)

if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients for samosa")
    print(response.content)