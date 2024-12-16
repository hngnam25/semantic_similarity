from langchain_core.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chat_models import ChatOpenAI
from typing import List, Dict
from scripts.logging_config import logger
import os
from dotenv import load_dotenv
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')
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

            self.llm = ChatOpenAI(
                model_name = model_name,
                temperature = temperature,
                max_tokens = max_tokens,
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
             # Construct the context from retrieved docs
             context = ""
             for idx, doc in enumerate(retrieved_docs, 1):
                context += f"{idx}. {doc['text']}\n\n"
            # Create a chat prompt template
             chat_prompt = ChatPromptTemplate.from_messages([
                            SystemMessagePromptTemplate.from_template(
                                "You are a helpful assistant. Use the following context to answer the question."
                            ),
                            HumanMessagePromptTemplate.from_template(
                                "Question: {question}\n\nContext:\n{context}\n\nAnswer:"
                            ),
             ])
            # Prepare the input variables
             input_variables = {
            "question": query,
            "context": context,
            }
             #Create an LLMChain
             chain = chat_prompt | self.llm

             #Generate the answere 
             answer = chain.invoke(input_variables)
             logger.info("LLM generated an answer succesfully")
             return answer.content.strip()
        except Exception as e:
            logger.error(f"Error getting answer: {e}")
            return "I'm sorry I could not generate an answerr at this time"
        

    