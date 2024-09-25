import os

from openai import OpenAI
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

from load_docs import load_api_data

PINECONE_KEY = os.getenv("PINECONE_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

index_name = "api-doc"

# 初始化Pinecone
pc = Pinecone(api_key=PINECONE_KEY)

index = pc.Index(index_name)
docs = load_api_data('docs/_rest-api.md')

client = OpenAI()   

def query_pinecone(text):
    query_embedding = client.embeddings.create(
        input=[text],
        model="text-embedding-3-large"
    ).data[0].embedding

    query_result = index.query(vector=query_embedding, top_k=5)
    docs_results = []
    for i in query_result.get('matches'):
        r = [k for k in docs if k['id'] == i['id']]
        docs_results.append(r[0]['text'])
    return docs_results

def enhance_response(query, docs):
    prompt = f"""
    You are an API support assistant. Please generate a concise, accurate, and customer-friendly response based on the following documentation to help them understand how to call the API.

    These are the related api documentations: 
    """


    for r in docs:
        prompt += f"{r}\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ]
    )

    return response.choices[0].message.content



def inference(query_text):
    query_result = query_pinecone(query_text)
    return enhance_response(query_text, query_result)