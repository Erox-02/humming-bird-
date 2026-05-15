# Prield – Ultra‑Light Privacy Firewall for LLM Prompts

**Prield** (Privacy + Shield) detects and masks Personally Identifiable 
Information (PII) in text before it reaches an LLM. It combines a trained 
sklearn ML classifier with a fast rule‑based masking engine.

## Features

- **ML‑powered detection**: sklearn pipeline with TF‑IDF for accurate PII identification
- **40+ PII categories**: emails, phones, credit cards, tokens, government IDs, medical IDs
- **Context‑preserving masking**: Placeholders like `[EMAIL_1]` replace secrets while keeping surrounding text
- **Metadata vault**: Maps placeholders back to original values for secure restoration
- **Dual API**: Simple `sanitize()` function or configurable `Pield` class
- **Microsecond inference**: Typical detection + masking in < 500µs for short texts
- **Minimal dependencies**: Only `joblib` and `scikit-learn`
- **Edge‑ready**: Lightweight enough for Raspberry Pi and similar devices

## Installation

```bash
pip install prield
