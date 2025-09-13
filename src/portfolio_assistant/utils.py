"""
Miscelelaneous support functions
"""
import logging
import sys


def configure_logging(level: str = "INFO"):
    """
    Set up logging for the application
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        stream=sys.stdout,
    )
    return logging.getLogger("portfolio-assistant")
