# MT-Evaluation-Project

A multi-stage machine translation (MT) evaluation framework using LLM-powered agents to assess translation quality across 17 error categories.

## Overview

This project implements a **three-stage evaluation pipeline** for machine translation quality assessment. It leverages large language models (GPT-4) to provide nuanced evaluation across 4 super-categories:

- **Semantic Equivalence** (6 categories)
- **Semantic Contradiction** (5 categories)
- **Grammatical & Morphological Distortion** (4 categories)
- **Information Completeness** (2 categories)

## Key Features

### Multi-Stage Agent Architecture
- **Stage 1**: Super-category evaluation - Identifies broad error types
- **Stage 2**: Sub-category evaluation - Detailed error classification with cross-verification
- **Stage 3**: Consistency verification - Validates agent agreements across evaluations

### Error Categories

**Similar Translation (Acceptable)**
- `Identical`, `Word_synm`, `Fluent`, `Mixd_lang`, `Negt_anto`, `Default_similar`

**Dissimilar Translation (Errors)**
- `Anto_flip`, `Negt_flip`, `Gend_flip`, `Sing_plul`, `Tens_chng`, `Word_ordr`, `Word_rplc`, `Add_extra`, `Omission`, `Neutral`, `Default_dissimilar`

## Project Structure

```
MT-Evaluation-Project/
├── own_framework.py                 # Core multi-agent framework
├── own_framework_prompts.py        # System prompts for all evaluation stages
├── own_framework_pipeline.py       # Batch processing pipeline
├── testing_on_indicMT_data.py     # Testing suite for IndicMT dataset
├── aggregation.py                  # Results aggregation and scoring
├── annotated_304.xlsx             # Sample annotated translations
├── Own_categories.txt             # Category definitions
├── requirements.txt               # Dependencies
└── Outputs_and_ErrorAnalysis/     # Results directory
```

## Quick Start

### Installation

```bash
git clone https://github.com/krishna404pandey/MT-Evaluation-Project.git
cd MT-Evaluation-Project
pip install -r requirements.txt
```

### Configuration

Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

### Basic Usage

```python
from own_framework import MTState, build_graph

state = MTState(
    source="The weather is beautiful today",
    mt="बहुत अच्छा मौसम आज है",
    reference="आज का मौसम बहुत सुंदर है"
)

graph = build_graph()
result = graph.invoke(state)
print(result["aggregation"])
```

### Batch Processing

```python
from own_framework_pipeline import evaluate_translations_batch

results = evaluate_translations_batch(
    df=translations_dataframe,
    source_col="source",
    mt_col="mt",
    reference_col="reference"
)
results.to_csv("evaluation_results.csv")
```

## Output Format

```json
{
  "accuracy_error": 0.15,
  "fluency_error": 0.05,
  "terminology_error": 0.10,
  "style_error": 0.08,
  "overall_error_probability": 0.12,
  "final_quality_score_100": 88.0
}
```

## Requirements

- Python 3.8+
- LangChain & LangGraph
- OpenAI API or Google Generative AI
- Pandas, NumPy, Pydantic

See `requirements.txt` for full list.

## Notes

- Requires valid API keys for OpenAI or Google Generative AI
- Works best with language pairs that have quality reference translations
- Evaluation costs scale with number of translations
- Optimized for English↔Indian language pairs
