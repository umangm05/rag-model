#!/bin/bash

# Script to pull the required Ollama model for embeddings
echo "Setting up Ollama embedding model..."

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
until curl -f http://localhost:11434/api/tags > /dev/null 2>&1; do
    echo "Waiting for Ollama..."
    sleep 5
done

echo "Ollama is ready. Pulling mxbai-embed-large model..."
ollama pull mxbai-embed-large

echo "Model pulled successfully!"
echo "You can now start the full application with: docker-compose up"

