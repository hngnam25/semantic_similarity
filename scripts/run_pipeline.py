
import argparse
from retrieval import retrieve_documents
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.generators.generator import LangChainGenerator
from  scripts.logging_config import logger


def main():
    parser = argparse.ArgumentParser(description="Run the full RAG pipeline.")
    parser.add_argument('--query', type=str, required=True, help='Natural language query')
    parser.add_argument('--method', type=str, choices=['sparse', 'dense', 'hybrid'], default='hybrid', help='Retrieval method')
    parser.add_argument('--faiss_index_file', type=str, default='data/embeddings/faiss_index.index', help='Path to FAISS index file')
    parser.add_argument('--metadata_file', type=str, default='data/embeddings/chunk_metadata.json', help='Path to metadata JSON file')
    parser.add_argument('--elasticsearch_index', type=str, default='legal_docs', help='Elasticsearch index name')
    parser.add_argument('--model_name', type=str, default='gpt-3.5-turbo', help='LLM model name')
    parser.add_argument('--top_k', type=int, default=5, help='Number of top chunks to retrieve')
    parser.add_argument('--output_file', type=str, default='results/answer.txt', help='Path to save the generated answer')

    args = parser.parse_args()

    # Step 1: Retrieve document chunks
    try:
        retrieved_chunks = retrieve_documents(
            query=args.query,
            method=args.method,
            faiss_index_file=args.faiss_index_file,
            metadata_file=args.metadata_file,
            elasticsearch_index=args.elasticsearch_index,
            top_k=args.top_k
        )
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        raise

    if not retrieved_chunks:
        logger.warning("No chunks retrieved. Generating a default response.")
        answer = "I'm sorry, I couldn't find relevant information to answer your question."
    else:
        # Step 2: Generate answer using LLM
        try:
            generator = LangChainGenerator(model_name=args.model_name)
            answer = generator.generate_answer(args.query, retrieved_chunks)
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise

    # Step 3: Save or print the answer
    try:
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(answer)
            logger.info(f"Generated answer saved to {args.output_file}")
        else:
            print("Generated Answer:")
            print(answer)
    except Exception as e:
        logger.error(f"Error saving or printing the answer: {e}")
        raise

if __name__ == '__main__':
    main()