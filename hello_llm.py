# import library
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# load environment variables
load_dotenv()

# Azure OpenAI configuration from .env
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# create Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

# create function to call hello llm
def hello_llm(prompt):
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    # print raw response    
    print("Raw response json:")
    print(response.model_dump_json(indent=2))
    # Check token usage
    token_usage = response.usage;
    print(f"\n--- THỐNG KÊ TOKEN [cite: 44] ---")
    print(f"Input token: {token_usage.prompt_tokens}, string length: {len(prompt)}")
    print(f"Output token: {token_usage.completion_tokens}, string length: {len(response.choices[0].message.content)}")
    print(f"Total token: {token_usage.total_tokens}")    
    return response.choices[0].message.content

# call the function
print(hello_llm("Hello, how are you?"))

# llm not have memory

