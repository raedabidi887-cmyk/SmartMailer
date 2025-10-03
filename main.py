"""
Main entry point for SmartMailer
"""

import sys
import argparse
from loguru import logger
from app.worker import SmartMailerWorker
from app.api import app
import uvicorn


def run_worker():
    """Run the email processing worker"""
    logger.info("Starting SmartMailer Worker...")
    worker = SmartMailerWorker()
    worker.start()


def run_api():
    """Run the FastAPI server"""
    logger.info("Starting SmartMailer API...")
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="SmartMailer - Application intelligente de gestion d'emails")
    parser.add_argument(
        "mode",
        choices=["worker", "api", "both"],
        help="Mode to run: worker (email processing), api (REST API), or both"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    logger.add(
        "logs/smartmailer.log",
        rotation="1 day",
        retention="30 days",
        level="DEBUG"
    )
    
    # Create logs directory
    import os
    os.makedirs("logs", exist_ok=True)
    
    try:
        if args.mode == "worker":
            run_worker()
        elif args.mode == "api":
            run_api()
        elif args.mode == "both":
            # Run both in separate processes
            import multiprocessing
            
            # Start worker process
            worker_process = multiprocessing.Process(target=run_worker)
            worker_process.start()
            
            # Start API process
            api_process = multiprocessing.Process(target=run_api)
            api_process.start()
            
            try:
                # Wait for both processes
                worker_process.join()
                api_process.join()
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                worker_process.terminate()
                api_process.terminate()
                worker_process.join()
                api_process.join()
                
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
