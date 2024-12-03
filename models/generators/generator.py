from langchain import PromptTemplate,LLMChain
from langchain.llms import OpenAI, HuggingFaceHub
from typing import List, Dict
from scripts.logging_config import logger
import os

class LangChainGenerator:
    def __init__(self, model_name: str = 'gpt-4o', temperature: float = 0.2, max_tokens: int = 500):
        """
        Initializes the LangChain generator with the specified model.

        Args:
            model_name (str): Name of the LLM model.
            temperature (float): Sampling temperature for the LLM.
            max_tokens (int): Maximum number of tokens to generate.
        """

        try:
            self.model_name = model_name
            self.temperature = temperature
            self.max_tokens = max_tokens

            self.llm = OpenAI(
                model_name = model_name,
                temperature = temperature,
                max_tokens = max_tokens,
                openai_api_keys = os.getenv('OPENAI_API_KEY')
            )
            logger.info(f"LLM initialized with model: '{model_name}'")
        except Exception as e:
            logger.error(f"Error initializing LangChain LLM: {e}")
            raise

    def generate_answer(self, query:str, retrieved_docs: List[Dict]) -> str:
        """
        Generates an answer using the LLM based on the query and retrieved documents.

        Args:
            query (str): The user's natural language query.
            retrieved_docs (List[Dict]): List of retrieved document chunks with metadata.

        Returns:
            str: Generated answer.
        """
        try: 
             #Construct the prompt 
             prompt = self.construct_prompt(query, retrieved_docs)
             logger.debug(f"Constructed prompt: '{prompt}'")

             #Create a prompt template
             prompt_template = PromptTemplate(
                   input_variables=["question", "context"],
                   template="Question: {question}\n\nRelevant Information:\n{context}\n\nAnswer:"
             )

             #Create an LLMChain
             chain = LLMChain(prompt=prompt_template, llm=self.llm)

             #Generate the answere 
             answer = chain.run()
             logger.info("LLM generated an answer succesfully")
             return answer.strip()
        except Exception as e:
            logger.error(f"Error getting answer: {e}")
            return "I'm sorry I could not generate an answerr at this time"
        
    def construct_prompt(query: str, retrieved_docs: List[Dict]) -> str:
        """
        Constructs a prompt for the LLM by combining the query with retrieved documents.

        Args:
            query (str): The user's natural language query.
            retrieved_docs (List[Dict]): List of retrieved document chunks with metadata.

        Returns:
            str: The constructed prompt.
        """
        prompt = f"Question: {query}\n\nRelevant Information:\n"
        for idx, doc in enumerate(retrieved_docs, 1):
            prompt += f"{idx}. {doc['text']}\n\n"
        prompt += "Answer:"
        return prompt

    