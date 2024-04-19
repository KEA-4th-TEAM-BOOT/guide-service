import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['AZURE_OPENAI_ENDPOINT'] = os.getenv('AZURE_OPENAI_ENDPOINT')
os.environ['OPENAI_API_TYPE'] = os.getenv('OPENAI_API_TYPE')
os.environ['OPENAI_API_VERSION'] = os.getenv('OPENAI_API_VERSION')
