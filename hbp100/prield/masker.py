"""Rule‑based masking engine that replaces sensitive values with placeholders."""

from collections import defaultdict
from typing import Dict, Tuple

from .patterns import PATTERNS, ORDERED_CATEGORIES


class Masker:
    """Applies regex patterns sequentially, replacing matches with numbered
    placeholders and collecting the original values in a metadata dictionary.
    
    The masking algorithm uses a two-pass approach:
    1. Collect all matches across all categories with their positions
    2. Replace from end to start to maintain index validity
    
    This ensures that overlapping patterns are handled correctly and that
    the final text preserves as much original context as possible.
    
    Example:
        >>> masker = Masker()
        >>> masked, meta = masker.mask("Email: john@example.com, OTP: 123456")
        >>> masked
        'Email: [EMAIL_1], OTP: [OTP_1]'
        >>> meta
        {'[EMAIL_1]': 'john@example.com', '[OTP_1]': '123456'}
    """

    def mask(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Scan *text* for PII, replace each occurrence with a placeholder,
        and return the masked text together with a ``{placeholder: original}`` mapping.

        The algorithm:
        1. Iterates through categories in ORDERED_CATEGORIES order
        2. For each match, generates a sequential placeholder ([CATEGORY_N])
        3. For keyword patterns, preserves the prefix and masks the value
        4. For simple patterns, replaces the entire match
        5. Sorts all matches by position (descending) for safe replacement
        6. Builds the metadata dictionary

        Args:
            text: Raw text that may contain sensitive information.

        Returns:
            A 2‑tuple of ``(masked_text, metadata)`` where metadata maps
            each placeholder to its original sensitive value.
        """
        # Phase 1: Collect all matches with their metadata
        matches = self._collect_matches(text)
        
        # Phase 2: Replace from end to start (maintains indices)
        masked_text, metadata = self._apply_replacements(text, matches)
        
        return masked_text, metadata

    def _collect_matches(self, text: str) -> list:
        """Find all PII matches in the text and record their positions.
        
        Returns:
            List of tuples: (start, end, placeholder, original_value)
        """
        matches = []
        counters: dict[str, int] = defaultdict(int)

        for category in ORDERED_CATEGORIES:
            pattern_info = PATTERNS[category]
            regex = pattern_info["regex"]
            has_groups = pattern_info["has_groups"]

            for match in regex.finditer(text):
                # Skip if this region was already matched by a higher-priority pattern
                if self._is_overlapping(match.start(), match.end(), matches):
                    continue
                    
                # Generate the next sequential placeholder
                counters[category] += 1
                placeholder = f"[{category}_{counters[category]}]"

                # Extract the original value based on pattern type
                if has_groups:
                    replacement = match.group(1) + placeholder
                    original = match.group(2)
                else:
                    replacement = placeholder
                    original = match.group(0)

                matches.append(
                    (match.start(), match.end(), replacement, original)
                )

        return matches

    def _is_overlapping(self, start: int, end: int, existing_matches: list) -> bool:
        """Check if a new match overlaps with any previously recorded match.
        
        This prevents lower-priority patterns from masking text that was
        already captured by a higher-priority pattern.
        """
        for ex_start, ex_end, _, _ in existing_matches:
            if start < ex_end and end > ex_start:
                return True
        return False

    def _apply_replacements(self, text: str, matches: list) -> Tuple[str, Dict[str, str]]:
        """Replace matches from end to start to maintain index validity.
        
        Args:
            text: Original text
            matches: List of (start, end, replacement, original)
            
        Returns:
            Tuple of (masked_text, metadata_dict)
        """
        # Sort by start position descending – critical for safe replacement
        matches.sort(key=lambda m: m[0], reverse=True)

        masked_text = text
        metadata: dict[str, str] = {}

        for start, end, replacement, original in matches:
            # Extract placeholder name from replacement string
            # Placeholder is always at the end, e.g., "[EMAIL_1]"
            ph_start = replacement.rfind("[")
            placeholder = replacement[ph_start:]
            
            metadata[placeholder] = original
            masked_text = masked_text[:start] + replacement + masked_text[end:]

        return masked_text, metadata
