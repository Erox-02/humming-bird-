"""Lightweight ML detector that uses a pre‑trained model (pridel.pkl).

The model is an sklearn pipeline that handles TF-IDF vectorization internally,
so we can pass raw text directly to its predict method.
"""

from importlib.resources import files
import joblib


class Detector:
    """Binary classifier that decides whether a text contains any PII.

    The underlying model is a sklearn pipeline that handles TF-IDF internally,
    meaning it expects raw strings and performs feature extraction as part of
    the pipeline.
    
    Attributes:
        model: The loaded sklearn pipeline with a ``predict`` method that
            accepts a list of strings and returns an array of predictions.
    """

    def __init__(self) -> None:
        """Load the serialized sklearn pipeline from the package resources."""
        model_path = files("prield") / "pridel.pkl"
        self.model = joblib.load(model_path)

    def has_pii(self, text: str) -> bool:
        """Return ``True`` if the text is predicted to contain PII.

        Args:
            text: Input string to classify. Can be any length since
                the TF-IDF vectorizer in the pipeline handles it.

        Returns:
            ``True`` if PII is detected, ``False`` otherwise.
            
        Example:
            >>> detector = Detector()
            >>> detector.has_pii("My email is john@example.com")
            True
            >>> detector.has_pii("Hello world")
            False
        """
        # The model (sklearn pipeline) expects a list of strings
        # and handles TF-IDF vectorization internally
        prediction = self.model.predict([text])[0]
        return bool(prediction)
