# Variables for paths
PYTHON = python
SCRIPTS_DIR = scripts

# Preprocessing task
preprocess:
	$(PYTHON) $(SCRIPTS_DIR)/preprocessing.py

# Indexing task
index:
	$(PYTHON) $(SCRIPTS_DIR)/index_documents.py

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
