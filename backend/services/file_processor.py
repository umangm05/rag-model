import os
import json
import pika
import logging
from typing import Dict, Any
from utils.document_loaders import process_and_index
from services.status_service import status_service

logger = logging.getLogger(__name__)

class FileProcessor:
    """Process files from the queue and create embeddings"""
    
    def __init__(self):
        self.status_service = status_service
    
    def process_file_message(self, ch, method, properties, body):
        """
        Process a file message from RabbitMQ queue
        
        Args:
            ch: Channel
            method: Method
            properties: Properties
            body: Message body (JSON string)
        """
        try:
            # Parse message
            message = json.loads(body)
            file_id = message.get("file_id")
            file_path = message.get("file_path")
            file_name = message.get("file_name")
            
            logger.info(f"Processing file: {file_name} (ID: {file_id})")
            
            # Update status to processing
            self.status_service.update_file_status(
                file_id=file_id,
                status="processing",
                progress=10,
                message="Starting file processing..."
            )
            
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Update status to parsing
            self.status_service.update_file_status(
                file_id=file_id,
                status="parsing",
                progress=30,
                message="Parsing document and creating chunks..."
            )
            
            # Process the file and create embeddings
            try:
                num_vectors, index_name = process_and_index(
                    file_path=file_path,
                    chunk_size=800,
                    chunk_overlap=120,
                    model="mxbai-embed-large"
                )
                
                # Update status to embedding
                self.status_service.update_file_status(
                    file_id=file_id,
                    status="embedding",
                    progress=70,
                    message=f"Creating embeddings... ({num_vectors} chunks)"
                )
                
                # Update status to completed
                self.status_service.update_file_status(
                    file_id=file_id,
                    status="completed",
                    progress=100,
                    message=f"File ready for chat! Processed {num_vectors} chunks into Pinecone index '{index_name}'"
                )
                
                logger.info(f"Successfully processed file {file_name}: {num_vectors} vectors created")
                
            except Exception as e:
                logger.error(f"Error processing file {file_name}: {e}")
                self.status_service.update_file_status(
                    file_id=file_id,
                    status="failed",
                    progress=0,
                    message="File processing failed",
                    error=str(e)
                )
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"Unexpected error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

# Global file processor instance
file_processor = FileProcessor()

