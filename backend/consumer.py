#!/usr/bin/env python3
"""
RabbitMQ Consumer for file processing
Run this script to start consuming file processing tasks
"""
import os
import logging
from dotenv import load_dotenv
from services.queue_service import queue_service
from services.file_processor import file_processor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Start the file processing consumer"""
    logger.info("Starting file processing consumer...")
    
    try:
        # Connect to RabbitMQ
        queue_service.connect()
        
        # Start consuming messages
        queue_service.consume_file_processing_tasks(
            callback=file_processor.process_file_message
        )
        
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user")
    except Exception as e:
        logger.error(f"Consumer error: {e}")
    finally:
        queue_service.disconnect()

if __name__ == "__main__":
    main()

