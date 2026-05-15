"""prield – Ultra-light privacy firewall .

Main Components:
    - Detector: ML-based PII detection using sklearn pipeline
    - Pield: Core sanitization engine with configurable masking
    - sanitize: Convenience function for quick one-shot sanitization

"""

from .core import sanitize, Pield
from .detector import Detector

__all__ = ["sanitize", "Pield", "Detector"]
__version__ = "0.1.0"
