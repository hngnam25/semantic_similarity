import json
from models.retrievers.elasticsearch_retriver import index_chunks_in_elasticsearch
from models.retriever.dense_retriever import compute_embeddings, build_faiss_index, save_faiss_index
from utils.logger import logger
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


def main(preprocessed_file: str, elasticsearch_index: str, faiss_index_file:str, meta_data_file:str):
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

        #Index in Elasticsearch
        from models.retrievers.elasticsearch_retriever import index_chunks_in_elasticsearch
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index documents for RAG system")
    parser.add_argument('--preprocessed_file', type=str, required=True, help='Path to preprocessed chunks JSONL file')
    parser.add_argument('--elasticsearch_index', type=str, default='legal_docs', help='Elasticsearch index name')
    parser.add_argument('--faiss_index_file', type=str, default='data/embeddings/faiss_index.index', help='Path to save FAISS index')
    parser.add_argument('--metadata_file', type=str, default='data/embeddings/chunk_metadata.json', help='Path to save metadata JSON file')

    args = parser.parse_args()
    main(args.preprocessed_file, args.elasticsearch_index, args.faiss_index_file, args.metadata_file)