import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.generators.generator import LangChainGenerator
from logging_config import logger
import json

def main(query: str, retrieved_chunks_file: str, output_file: str = None, model_name: str = 'gpt-4o'):
    """
    Main function to generate an answer using the LangChain LLM.

    Args:
        query (str): The user's natural language query.
        retrieved_docs_file (str): Path to the JSON file containing retrieved documents.
        output_file (str, optional): Path to save the generated answer. Defaults to None.
        model_name (str, optional): Name of the LLM model. Defaults to 'gpt-3.5-turbo'.

    Returns:
        None
    """
    try:
        #Load retrieved chunks
        with open(retrieved_chunks_file, 'r', encoding='utf-8') as f:
            retrieved_chunks=json.load(f)
        logger.info(f"Loaded {len(retrieved_chunks)} retrieved chunks from {retrieved_chunks_file}")

        #Initialize generator
        generator = LangChainGenerator(model_name=model_name)

        #Generate the answer
        answer = generator.generate_answer(query, retrieved_chunks)

        #Output the answer 
        if output_file:
            with open(output_file,'w', encoding ='utf-8') as f:
                f.write(answer)
            logger.info(f"Generated answer saved to {output_file}")
        
        else:
            print("Generated Answer:")
            print(answer)

    except Exception as e:
        logger.error(f"Generation failed: {e}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate answer using LangChain LLM")
    parser.add_argument('--query', type=str, required=True, help='Natural language query')
    parser.add_argument('--retrieved_chunks_file', type=str, required=True, help='Path to retrieved chunks JSON file')
    parser.add_argument('--output_file', type=str, default=None, help='Path to save the generated answer')
    parser.add_argument('--model_name', type=str, default='gpt-4o', help='LLM model name')

    args = parser.parse_args()
    main(args.query, args.retrieved_chunks_file, args.output_file, args.model_name)