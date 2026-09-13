from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.5",
    input="Say hello and tell me you are ready to analyze resumes."
)

print(response.output_text)