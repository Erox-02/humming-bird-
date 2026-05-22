# 🐦 hbp100 — Hummingbird Precision 100

**322KB. 0.77ms. 100% precision. Faster than you blink.**

[![PyPI version](https://badge.fury.io/py/hbp100.svg)](https://pypi.org/project/hbp100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Install

```bash
pip install hbp100
Use
python
from hbp100 import sanitize

result = sanitize("My email is john@gmail.com")
print(result.text)      # "My email is [EMAIL_1]"
print(result.metadata)  # {'[EMAIL_1]': 'john@gmail.com'}
Numbers
Metric	Value
Package size	322KB
Inference	0.77ms
Precision	100%
F1 Score	84%
PII types	40+
Context-Aware
Input	Output
"What's my zodiac for 1990?"	"What's my zodiac for 1990?" (year kept)
"I was born in 1990"	"I was born in [YEAR_ONLY_1]" (year masked)
Why hbp100?
Microsoft Presidio	hbp100
Size	70MB	322KB
Precision	85-90%	100%
Latency	10-50ms	0.77ms
Context-aware	❌	✅
Edge-ready	❌	✅
License
MIT

