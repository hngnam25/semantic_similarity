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


# Retrieval task
retrieve:
	$(PYTHON) $(SCRIPTS_DIR)/retrieve.py

# Generation task
generate:
	$(PYTHON) $(SCRIPTS_DIR)/generate.py

# Run full pipeline
pipeline: preprocess index retrieve generate

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
