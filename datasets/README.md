# Downloaded Datasets

This directory contains datasets for the research project. Data files are NOT
committed to git due to size. Follow the download instructions below.

## Dataset 1: OpenReview ICLR Peer Reviews

### Overview
- **Source**: HuggingFace dataset `smallari/openreview-iclr-peer-reviews`
- **Size**: 19,076 examples
- **Format**: HuggingFace Dataset (single split: `raw`)
- **Task**: Peer review analysis, scoring, and review generation
- **Fields**: venue, year, paper_id, title, abstract, decision, label, reviews
- **License**: Not specified in dataset card

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset

dataset = load_dataset("smallari/openreview-iclr-peer-reviews")
dataset.save_to_disk("datasets/openreview_iclr_peer_reviews")
```

### Loading the Dataset
```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/openreview_iclr_peer_reviews")
```

### Sample Data
`datasets/openreview_iclr_peer_reviews/samples/sample.json`

### Notes
- Suitable for studying review content, scores, and decisions.
- Reviews are nested within the `reviews` field.

## Dataset 2: ICLR Peer Reviews (LLM + Human)

### Overview
- **Source**: HuggingFace dataset `JerMa88/ICLR_Peer_Reviews`
- **Size**: 15,821 examples
- **Format**: HuggingFace Dataset (split: `train`)
- **Task**: Peer review quality analysis and LLM detection
- **Fields**: title, abstract, full_text, review, year, overall_score, thinking_trace, prompt, etc.
- **License**: Not specified in dataset card

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset

dataset = load_dataset("JerMa88/ICLR_Peer_Reviews")
dataset.save_to_disk("datasets/iclr_peer_reviews")
```

### Loading the Dataset
```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/iclr_peer_reviews")
```

### Sample Data
`datasets/iclr_peer_reviews/samples/sample.json`

### Notes
- Includes LLM-generated traces and metadata useful for AI-vs-human review analysis.
