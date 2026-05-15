"""Core pipeline: detector → (optional reasoner) → masker.

This module provides both a simple functional interface and an 
object-oriented interface that allows configuration per instance.
"""

from typing import Optional
from .detector import Detector
from .masker import Masker
from .schemas import SanitizeResult


class Pield:
    """Main privacy firewall engine with configurable components.
    
    This class allows creating multiple instances with different 
    configurations, such as using different detector models or
    enabling/disabling specific masking rules.
    
    The name "Pield" combines "Privacy" + "Shield" – it's the
    firewall that protects your LLM prompts from leaking PII.
    
    Attributes:
        detector: The ML detector instance for PII classification.
        masker: The rule-based masking engine.
        
    Example:
        >>> # Default usage
        >>> pield = Pield()
        >>> result = pield.sanitize("My email is john@example.com")
        >>> print(result.has_pii)
        True
        
        >>> # Custom configuration for financial domain
        >>> finance_detector = Detector()  # Could load finance-specific model
        >>> finance_pield = Pield(detector=finance_detector)
        >>> result = finance_pield.sanitize("Account: 1234567890")
    """
    
    def __init__(self, detector: Optional[Detector] = None) -> None:
        """Initialize the privacy firewall with optional custom detector.
        
        Args:
            detector: Optional pre-configured Detector instance. If None,
                creates a default detector that loads the bundled model.
                
        Note:
            Each Pield instance creates its own Masker. If you need
            multiple instances, consider reusing detectors to avoid
            loading the model multiple times.
        """
        self.detector = detector or Detector()
        self.masker = Masker()
    
    def sanitize(self, text: str) -> SanitizeResult:
        """Run the full privacy firewall pipeline on *text*.

        Pipeline stages:
        1. **Detection**: ML model checks if text contains PII
        2. **(Future) Reasoning**: Context-aware masking decisions
        3. **Masking**: Rule-based pattern replacement

        If no PII is detected in stage 1, the original text is returned
        unchanged with an empty metadata dictionary. This short-circuit
        avoids the overhead of regex processing for clean text.

        Args:
            text: The raw input string (e.g., an LLM prompt). Can be
                any length – the detector and masker both handle
                variable-length inputs.

        Returns:
            A ``SanitizeResult`` containing:
            - ``text``: The (possibly) masked text
            - ``metadata``: Mapping of placeholders to original values
            - ``has_pii``: The detector's boolean classification
            
        Example:
            >>> pield = Pield()
            >>> result = pield.sanitize("OTP: 123456 and email: john@example.com")
            >>> result.text
            'OTP: [OTP_1] and email: [EMAIL_1]'
            >>> result.metadata
            {'[OTP_1]': '123456', '[EMAIL_1]': 'john@example.com'}
            >>> result.has_pii
            True
        """
        # Stage 1: ML-based PII detection
        if not self.detector.has_pii(text):
            return SanitizeResult(text=text, metadata={}, has_pii=False)
        
        # FUTURE: Stage 2 – Insert Reasoner here
        # The reasoner could:
        # - Determine which categories to mask based on context
        # - Apply user consent preferences
        # - Handle domain-specific logic
        # reasoner = Reasoner()
        # mask_categories = reasoner.decide(text, self.detector)
        
        # Stage 3: Rule-based masking
        masked_text, metadata = self.masker.mask(text)
        return SanitizeResult(
            text=masked_text, 
            metadata=metadata, 
            has_pii=True
        )


# Module-level convenience instance for the functional API
# Created once at import time – model is loaded into memory
_default_pield = Pield()


def sanitize(text: str) -> SanitizeResult:
    """Convenience function for one-shot sanitization using the default engine.
    
    This is the simplest way to use prield:
    
        >>> from prield import sanitize
        >>> result = sanitize("My email is john@example.com")
        >>> print(result.text)
        'My email is [EMAIL_1]'
    
    It uses a module-level Pield instance that's created once and reused.
    For advanced use cases (multiple models, custom configurations), use
    the Pield class directly.
    
    Args:
        text: The raw input string to sanitize.

    Returns:
        A ``SanitizeResult`` with the sanitized text and metadata.
        
    Performance Note:
        The first call loads the ML model (~10-50ms). Subsequent calls
        are fast (~100-500µs for typical inputs).
    """
    return _default_pield.sanitize(text)
