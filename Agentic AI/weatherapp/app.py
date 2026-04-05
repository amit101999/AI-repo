from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def main():
    user_query = input()