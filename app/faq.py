import pandas as pd
from pathlib import Path
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os


load_dotenv()

# os.environ["GROQ_MODEL_NAME"]

faq_path = Path(__file__).parent / "resources/faq_data.csv"

client = chromadb.Client()
collection_name_faq = "faqs"
groq_client = Groq()

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in client.list_collections()]: 
        print("Ingestiong FAQ data in chromadb...")
        collection = client.get_or_create_collection(
            name=collection_name_faq,
            embedding_function=ef
        )
        df = pd.read_csv(path)
        docs = df["question"].tolist()
        metadata = [{'answer':ans} for ans in df['answer'].to_list()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collection.add(
            documents=docs,
            metadatas=metadata,
            ids = ids
        )
    else:
        print(f"Collection {collection_name_faq} already exists. Skipping ingestion.")

def get_relevant_qa(query):
    collection = client.get_collection(name=collection_name_faq)
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results


def faq_chain(query):
    result = get_relevant_qa(query)
    context = " ".join([item.get('answer') for item in result['metadatas'][0]])
    answer = generate_answer(query, context)
    return answer

def generate_answer(query, context):
    prompt = f'''Given the question and context below, generate the answer based on the context only.
    if you don't find the answer inside then context then say "I don't know"
    Do not make up an answer.
    QUESTION: {query}
    CONTEXT: {context}
    '''
    # call llm
    chat_completion = groq_client.chat.completions.create(
        messages = [
            {
                "role":"user",
                "content":prompt,
            }
        ],
        model = os.environ["GROQ_MODEL"],
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    ingest_faq_data(faq_path)
    query = "is it suitable for intenational shipping?"
    # results = get_relevant_qa(query)
    # print(results)
    # print(faq_path)
    answer = faq_chain(query)
    print(answer)