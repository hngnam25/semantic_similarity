import uuid

def create_chunk_metadata(document_id, chunk_index, heading=None):
    chunk_id = f"{document_id}_{chunk_index}"
    metadata = {
        'document_id': document_id,
        'chunk_id': chunk_id,
        'heading': heading,
    }
    return metadata