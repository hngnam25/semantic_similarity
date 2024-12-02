from elasticsearch import Elasticsearch, helpers
from typing import List, Dict
from utils.logger import logger


def query_elasticsearch(query_text:str, index_name:str, host: str = 'localhost', port: int = 9200 , top_k: int = 10) -> List[Dict]:
    """
    Queries the Elasticsearch index and retrieves the top-k relevant documents.

    Args:
        query_text (str): The search query.
        index_name (str): The name of the Elasticsearch index.
        host (str): Elasticsearch host address.
        port (int): Elasticsearch port number.
        top_k (int): Number of top documents to retrieve.

    Returns:
        List[Dict]: A list of dictionaries containing retrieved documents and their metadata.
    """
    try:
        es = Elasticsearch([{'host':host, 'port': port}])
        logger.info(f"Connected to Elasticsearch at {host}:{port}")

        #Define search query
        search_query = {
            "query": {
                "match": {
                    "text": {
                        "query": query_text,
                        "operator": "and"
                    }
                }
            },
            "size": top_k
        }

        #Execute the search 
        response = es.search(index = index_name , body= search_query)
        logger.info(f"Elasticsearch query executed successfully for query: '{query_text}'")


        #Extract the results
        hits = response['hits']['hits']
        results = []
        for hit in hits:
            source = hit['_source']
            score = hit['_score']
            result = {
                'chunk_id': source.get('chunk_id'),
                'document_id': source.get('document_id'),
                'heading': source.get('heading'),
                'text': source.get('text'),
                'score': score
            }
            results.append(result)
        logger.info(f"Retrieved{len(results)} documents from Elasticsearch")
        return results
    
    #throw exception if query fails
    except Exception as e:
        logger.error(f"Error querying Elasticsearch: {e}")
        return[]

# def index_chunks_in_elasticsearch(chunks, index_name = 'legal_docs'):
#     es = Elasticsearch()

#     #Create index, if it doesn't exist
#     if not es.indices.exists(index = index_name):
#         es.indices.create(index = index_name)
    
#     # Perfroms bulk indexing of documents into ElasticSearch
#     actions = [
#         {
#             "_index": index_name,
#             "_id": chunk['chunk_id'],
#             "_source": chunk
#         }
#         for chunk in chunks
#     ]
#     helpers.bulk(es,actions)

# def query_elasticsearch(query_text, index_name = )