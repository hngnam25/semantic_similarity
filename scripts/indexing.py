import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.retrievers.elasticsearch_retriever import index_chunks_in_elasticsearch  
from models.retrievers.dense_retriever import compute_embeddings, build_faiss_index, save_faiss_index
from logging_config import logger
import argparse



def load_preprocessed_chunks(preprocessed_file: str) -> list:
    """
    Loads preprocessed chunks from a JSONL file.

    Args:
        preprocessed_file (str): Path to the JSONL file.

    Returns:
        list: List of chunk dictionaries.
    """
    try:
        chunks = []
        with open(preprocessed_file, 'r', encoding = 'utf-8') as f:
            for line in f:
                chunks.append(json.loads(line))
        logger.info(f"Loaded {len(chunks)} preprocessed chunks from {preprocessed_file}")
        return chunks
    except Exception as e:
        logger.error(f"Error loading preprocessed chunks: {e}")
        raise

def save_metadata(metadata: list, metadata_file: str):
    """
    Saves metadata to a JSON file.

    Args:
        metadata (list): List of metadata dictionaries.
        metadata_file (str): Path to the metadata JSON file.

    Returns:
        None
    """
    try:
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved to {metadata_file}")
    except Exception as e:
        logger.error(f"Error saving metadata: {e}")
        raise


def main(preprocessed_file: str, elasticsearch_index: str, faiss_index_file:str, metadata_file:str):
    """
    Main function to index documents.

        Args:
            preprocessed_file (str): Path to the preprocessed JSONL file.
            elasticsearch_index (str): Name of the Elasticsearch index.
            faiss_index_file (str): Path to save the FAISS index.
            metadata_file (str): Path to save the metadata JSON file.

        Returns:
            None
    """
    try: 
        #Load preprocessed chunks
        chunks = load_preprocessed_chunks(preprocessed_file)

        index_chunks_in_elasticsearch(chunks, index_name=elasticsearch_index)

        #Compute embeddings for FAISS
        embeddings = compute_embeddings(chunks)

        #Build FAISS index
        faiss_index = build_faiss_index(embeddings)

        #Save FAISS index and metadata
        save_faiss_index(faiss_index, faiss_index_file)
        save_metadata(chunks, metadata_file)

    except Exception as e:
        logger.error(f"Indexing failed: {e}")
def preprocess_data():
    logger.info("Starting the indexing pipeline.")
    try:
        # Your preprocessing logic
        logger.debug("Indexing raw data successfully.")
        # Simulating an error
        raise ValueError("An error occurred during indexiong.")
    except Exception as e:
        logger.error(f"Error in preprocessing: {e}")
        raise

if __name__ == "__main__":
    logger.info("Script started.")
    parser = argparse.ArgumentParser(description="Index documents for RAG system")
    parser.add_argument('--preprocessed_file', type=str, required=True, help='Path to preprocessed chunks JSONL file')
    parser.add_argument('--elasticsearch_index', type=str, default='legal_docs', help='Elasticsearch index name')
    parser.add_argument('--faiss_index_file', type=str, default='data/embeddings/faiss_index.index', help='Path to save FAISS index')
    parser.add_argument('--metadata_file', type=str, default='data/embeddings/chunk_metadata.json', help='Path to save metadata JSON file')
    parser.add_argument('--elasticsearch_url', type=str, required=True, help='URL of the Elasticsearch instance')
    args = parser.parse_args()
    main(args.preprocessed_file, args.elasticsearch_index, args.faiss_index_file, args.metadata_file)
    # preprocess_data()

    logger.info("Script finished.")