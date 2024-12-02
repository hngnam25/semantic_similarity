import os
from utils.html_parser import parse_html, extract_main_content
from utils.chunker import fixed_length_chunking
from utils.helper import create_chunk_metadata
from utils.text_cleaner import clean_text

def save_chunks_to_jsonl(chunks, output_file):
    # Import json here - this is unusual, typically imports should be at the top
    # Consider moving this import to the top of the file
    import json
    
    # Open file in write mode with UTF-8 encoding to handle special characters
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write each chunk as a separate line in JSONL format
        for chunk in chunks:
            f.write(json.dumps(chunk) + '\n')

def process_documents(input_dir, output_file):
    all_chunks = []
    doc_counter = 0
    for filename in os.listdir(input_dir):
        if filename.endswith('.html'):
            doc_counter+=1
            print(doc_counter)
            file_path = os.path.join(input_dir, filename)
            document_id = os.path.splitext(filename)[0]

            # Parse HTML and extract text
            soup = parse_html(file_path)
            main_text = extract_main_content(soup)
            clean_main_text = clean_text(main_text)

            # Choose chunking method
            # Option 1: Paragraphs
            # chunks = split_by_paragraphs(soup)
            # Option 2: Headings
            # chunks_with_headings = split_by_headings(soup)
            # Option 3: Fixed-Length
            chunks = fixed_length_chunking(clean_main_text)

            # Process and add metadata
            for idx, chunk in enumerate(chunks):
                chunk_text = clean_text(chunk)
                if chunk_text:
                    metadata = create_chunk_metadata(document_id, idx)
                    chunk_data = {
                        'text': chunk_text,
                        **metadata
                    }
                    all_chunks.append(chunk_data)
    # Save all chunks to a JSONL file
    save_chunks_to_jsonl(all_chunks, output_file)
