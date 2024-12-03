import argparse
import json 
from typing import List, Dict
from models.retrievers.elasticsearch_retriever import query_elasticsearch
from models.retrievers.dense_retriever import load_faiss_index, query_faiss_index
from sentence_transformers import SentenceTransformer
from logging_config import logger



def retrieve_documents(query:str, method:str, faiss_index_file: str, metadata_file: str, elasticsearch_index: str, top_k: int) -> List[Dict]:
    """
    Retrieves relevant document chunks based on the query.

    Args:
        query (str): The user's natural language query.
        method (str): Retrieval method ('sparse', 'dense', 'hybrid').
        faiss_index_file (str): Path to the FAISS index file.
        metadata_file (str): Path to the metadata JSON file.
        elasticsearch_index (str): Name of the Elasticsearch index.
        top_k (int): Number of top chunks to retrieve.

    Returns:
        List[Dict]: List of retrieved document chunks.
    """

    retrieved_chunks = []

    if method in ['sparse']:
        #Sparse Retrieval using Elasticsearch
        sparse_results = query_elasticsearch(query_text=query, index_name=elasticsearch_index, top_k = top_k)
        retrieved_chunks.extend(sparse_results)
        logger.info(f"Sparse retrieval returned {len(sparse_results)} chunks")

    if method in ['dense']:
        #Desne Retrieval using FAISS

        #Load FAISS index
        faiss_index= load_faiss_index(faiss_index_file)

        #Load metadata
        with open(metadata_file, 'r', encoding = 'utf-8') as f:
            metadata = json.load(f)
        logger.info("Loaded metadata for dense retrieval from {metadata_file}")

        #Initialize embedding model 
        model = SentenceTransformer('all-MiniLM-L6-v2')


        #Query FAISS index
        dense_results = query_faiss_index(query_text=query, index=faiss_index, model=model, metadata=metadata, top_k= top_k)
        retrieved_chunks.extend(dense_results)
    
    #If hybrid, consider removing duplicates or reranking
    if method == 'hybrid':
        #Remove duplicates based on 'chunk_id'
        unique_chunks = {chunk['chunk_id']: chunk for chunk in retrieved_chunks}
        retrieved_chunks = list(unique_chunks.values())
        logger.info(f"Hybrid retrieval consolidated to {len(retrieved_chunks)} unique chunks.")
    
    return retrieved_chunks


def main():
    parser = argparse.ArgumentParser(description="Retrieve document chunks based on a query.")
    parser.add_argument('--query', type=str, required=True, help='Natural language query')
    parser.add_argument('--method', type=str, choices=['sparse', 'dense', 'hybrid'], default='sparse', help='Retrieval method')
    parser.add_argument('--faiss_index_file', type=str, default='data/embeddings/faiss_index.index', help='Path to FAISS index file')
    parser.add_argument('--metadata_file', type=str, default='data/embeddings/chunk_metadata.json', help='Path to metadata JSON file')
    parser.add_argument('--elasticsearch_index', type=str, default='legal_docs', help='Elasticsearch index name')
    parser.add_argument('--top_k', type=int, default=5, help='Number of top chunks to retrieve')
    parser.add_argument('--output_file', type=str, default='data/retrieved_chunks.json', help='Path to save retrieved chunks')

    args = parser.parse_args()

    # Retrieve document chunks
    retrieved_chunks = retrieve_documents(
        query=args.query,
        method=args.method,
        faiss_index_file=args.faiss_index_file,
        metadata_file=args.metadata_file,
        elasticsearch_index=args.elasticsearch_index,
        top_k=args.top_k
    )
    # Save retrieved chunks to a file
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(retrieved_chunks, f, indent=2)
    logger.info(f"Retrieved chunks saved to {args.output_file}")

if __name__ == '__main__':
    main()
