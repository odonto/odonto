import logging
import os
logger = logging.getLogger(
    os.path.basename(os.path.dirname(__file__))
)
__all__ = [
    "logger"
]