from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os 
from typing import List, Dict
from utils.logger import logger


def compute_embeddings(chunks: List[Dict], model_name = 'all-MiniLM-L6-V2') -> np.ndarray:
    """
    Computes embeddings for each text chunk using Sentence-BERT.

    Args:
        chunks (List[Dict]): List of text chunks with metadata.
        model_name (str): Pretrained SentenceTransformer model name.

    Returns:
        np.ndarray: Array of embeddings.
    """
    try:
        model = SentenceTransformer(model_name)
        texts = [chunk['text'] for chunk in chunks]
        embeddings = model.encode(texts, show_progress_bar = True)
        logger.info(f"Computed embeddings for {len(chunks)} chunks using model'{model_name}'")
        return embeddings
    
    except Exception as e:
        logger.error(f"Error computing embeddings: {e}")
        raise

def build_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """
    Builds a FAISS index from embeddings.

    Args:
        embeddings (np.ndarray): Array of embeddings.

    Returns:
        faiss.Index: The FAISS index object.
    """
    try:
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        logger.info(f"FAISS index built with {index.ntotal} vectors")
        return index
    
    except Exception as e: 
        logger.error(f"Error building FAISS index: {e}")
        raise

def save_faiss_index(index: faiss.Index, index_file_path: str):
    """
    Saves a FAISS index to disk.

    Args:
        index (faiss.Index): The FAISS index object.
        index_file_path (str): File path to save the index.

    Returns:
        None
    """
    try:
        directory = os.path.dirname(index_file_path)
        if directory and not os.path.exist(directory):
            os.makedirs(directory, exist_ok = True)
            logger.info(f"Created directory '{directory}' for FAISS index")

        faiss.write_index(index, index_file_path)
        logger.info(f"FAISS index saved to {index_file_path}")

    except Exception as e:
        logger.error(f"Error saving FAISS index: {e}")
        raise


def load_faiss_index(index_file_path:str) -> faiss.Index:
    """
    Loads a FAISS index from disk.

    Args:
        index_file_path (str): File path of the saved index.

    Returns:
        faiss.Index: The loaded FAISS index object.
    """
    try:
        if not os.path.exists(index_file_path):
            raise FileNotFoundError(f"FAISS index file not found at {index_file_path}")

        index = faiss.read_index(index_file_path)
        logger.info(f"FAISS index loaded from {index_file_path}")
        return index
    except Exception as e:
        logger.error(f"Error loading FAISS index: {e}")
        raise


def query_faiss_index(query_text: str, index: faiss.Index, model: SentenceTransformer, metadata: List[Dict], top_k: int = 15) -> List[Dict]:
    """
    Queries the FAISS index to retrieve the most similar documents.

    Args:
        query_text (str): The search query.
        index (faiss.Index): The FAISS index object.
        model (SentenceTransformer): The embedding model.
        metadata (List[Dict]): List of metadata dictionaries corresponding to the index.
        top_k (int): Number of top documents to retrieve.

    Returns:
        List[Dict]: A list of dictionaries containing retrieved documents and their metadata.
    """

    try: 
        query_embedding = model.encode([query_text])
        distances, indices = index.search(np.array(query_embedding), top_k)
        logger.info(f"FAISS query executed succesfully for query: '{query_text}")

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(metadata):
                doc_metadata = metadata[idx]
                result = {
                    'chunk_id': doc_metadata.get('chunk_id'),
                    'document_id': doc_metadata.get('document_id'),
                    'heading': doc_metadata.get('heading'),
                    'text': doc_metadata.get('text'),
                    'score': float(distance)
                }
                results.append(result)
            else:
                logger.warning(f"Index {idx} is out of bounds for metadatalist")
            
        logger.info(f"Index {idx} is out of bounds for metadata list")
        return results
    
    except Exception as e:
        logger.error(f"Error querying FAISS index: {e}")
        return[]