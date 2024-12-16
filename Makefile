# Variables for paths
PYTHON = python
SCRIPTS_DIR = scripts
VENV = venv
include .env
# Create and activate virtual environment
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip

install_dependencies: $(VENV)/bin/activate
	$(VENV)/bin/pip install -r requirements.txt
# Start Elasticsearch service (adjust command based on your system)
start_elasticsearch:
	# For example, if using systemctl on Linux
	sudo systemctl start elasticsearch
METHOD ?= "dense"
FAISS_INDEX_FILE ?= "data/embeddings/faiss_index.index"
METADATA_FILE ?= "data/embeddings/chunk_metadata.json"
ELASTICSEARCH_INDEX ?= "legal_docs"
MODEL_NAME ?= "gpt-4o"
TOP_K ?= 15
RETRIEVER_OUTPUT_FILE ?= "results/retriever_output.jsonl"
RETRIEVED_CHUNKS_FILE ?= "results/retriever_output.jsonl"
GENERATOR_OUTPUT_FILE ?= "results/generator_output.jsonl"
QUERY ?= ""

# Index the processed chunks
index:
	@echo "Using Elasticsearch URL: $(ELASTICSEARCH_URL)"
	python scripts/indexing.py \
	  --preprocessed_file data/preprocessed/processed_chunks.jsonl \
	  --elasticsearch_index legal_docs \
	  --faiss_index_file data/embeddings/faiss_index.index \
	  --metadata_file data/embeddings/chunk_metadata.json \
	  --elasticsearch_url $(ELASTICSEARCH_URL)
# Preprocessing task
preprocess:
	$(PYTHON) $(SCRIPTS_DIR)/preprocessing.py


# Run retrieval script
retrieve_documents:
	python scripts/retrieval.py --query "$(QUERY)" --method "$(METHOD)" --faiss_index_file "$(FAISS_INDEX_FILE)" --metadata_file "$(METADATA_FILE)" --elasticsearch_index "$(ELASTICSEARCH_INDEX)" --top_k "$(TOP_K)" --output_file "$(OUTPUT_FILE)"

# Run generator script
generate_answer:
	python scripts/generator.py --query "$(QUERY)" --retrieved_chunks_file "$(RETRIEVED_CHUNKS_FILE)" --output_file "$(GENERATOR_OUTPUT_FILE)" --model_name "$(MODEL_NAME)"

# Run full pipeline script
run_pipeline:
	python scripts/run_pipeline.py --query "$(QUERY)" --method "$(METHOD)" --faiss_index_file "$(FAISS_INDEX_FILE)" --metadata_file "$(METADATA_FILE)" --elasticsearch_index "$(ELASTICSEARCH_INDEX)" --model_name "$(MODEL_NAME)" --top_k "$(TOP_K)" --output_file "$(OUTPUT_FILE)"

# Install dependencies
install:
	pip install -r requirements.txt

# Clean up intermediate files
clean:
	rm -rf data/preprocessed/* data/embeddings/* results/*

# Help menu
help:
	@echo "Usage:"
	@echo "  make preprocess   - Run preprocessing script"
	@echo "  make index        - Index documents for retrieval"
	@echo "  make retrieve     - Retrieve relevant documents"
	@echo "  make generate     - Generate responses"
	@echo "  make pipeline     - Run the full RAG pipeline"
	@echo "  make install      - Install dependencies"
	@echo "  make clean        - Clean intermediate files"
