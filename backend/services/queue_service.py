import os
import json
import pika
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class QueueService:
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.queue_name = os.getenv("RABBITMQ_QUEUE_NAME", "file_processing_queue")
        self.connection = None
        self.channel = None
        
    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            logger.info(f"Connected to RabbitMQ queue: {self.queue_name}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def disconnect(self):
        """Close RabbitMQ connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Disconnected from RabbitMQ")
    
    def publish_file_processing_task(self, file_data: Dict[str, Any]) -> bool:
        """
        Publish a file processing task to the queue
        
        Args:
            file_data: Dictionary containing file information
                - file_id: Unique file identifier
                - file_path: Path to the uploaded file
                - file_name: Original filename
                - file_type: MIME type
                - file_size: File size in bytes
        
        Returns:
            bool: True if message was published successfully
        """
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()
            
            # Add timestamp to the message
            message = {
                **file_data,
                "timestamp": datetime.now().isoformat(),
                "status": "queued"
            }
            
            # Publish message with persistence
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            
            logger.info(f"Published file processing task for file_id: {file_data.get('file_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return False
    
    def consume_file_processing_tasks(self, callback):
        """
        Start consuming messages from the queue
        
        Args:
            callback: Function to handle incoming messages
        """
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()
            
            # Set up consumer
            self.channel.basic_qos(prefetch_count=1)  # Process one message at a time
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=callback
            )
            
            logger.info("Starting to consume file processing tasks...")
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            self.channel.stop_consuming()
            self.disconnect()
        except Exception as e:
            logger.error(f"Error in consumer: {e}")
            raise

# Global queue service instance
queue_service = QueueService()
