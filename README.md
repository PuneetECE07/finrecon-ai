# FinRecon AI — Autonomous Finance Reconciliation Agent

FinRecon AI automates reconciliation across payment transactions, settlement
records, and bank records. It matches high-confidence records, detects
discrepancies, classifies exceptions, calculates measurable reconciliation
metrics, and provides AI-assisted explanations for finance operators.

> **Razorpay AI Finance Controller Track**
>
> Demo data is synthetic and contains 120 transaction records.

## Problem

Finance operations teams often reconcile payment, settlement, and bank records
manually. Missing entries, amount mismatches and duplicates can require
time-consuming investigation.

## Solution

FinRecon AI creates one reconciliation loop:

```text
Payment Records
      ↓
Data Normalization
      ↓
Deterministic Reconciliation Engine
      ↓
Match / Exception Detection
      ↓
AI Exception Analyst
      ↓
Metrics + Auditable Report
```

## Features

- Reconciles 120 synthetic transaction records
- Payment vs settlement vs bank comparison
- Missing-record detection
- Amount-mismatch detection
- Duplicate bank-record detection
- Match-rate calculation
- Exception categorization
- Downloadable reconciliation report
- AI-assisted exception explanations
- Deterministic fallback when no LLM API key is configured
- Automated unit tests

## Tech Stack

- Python
- Pandas
- Streamlit
- OpenAI API (optional)
- Pytest

## Run locally

```bash
git clone https://github.com/PuneetECE07/finrecon-ai.git
cd finrecon-ai

python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## Optional AI setup

Copy `.env.example` to `.env` and set an API key.

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

The application still works without an API key using a deterministic
exception-analysis fallback.

## Evaluation

The dashboard calculates:

- Total records
- Matched records
- Exception records
- Match rate
- Exception category counts

All values are calculated from the dataset at runtime rather than hard-coded.

## Exception handling

FinRecon AI deliberately does not force ambiguous records into a match.
Exceptions are surfaced for review with a reason and recommended action.

## Safety / data note

All records in this repository are synthetic. No real customer, payment,
banking, or personally identifiable financial data is included.

## Project structure

```text
finrecon-ai/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   ├── transactions.csv
│   ├── settlements.csv
│   └── bank_records.csv
├── src/
│   ├── reconciliation.py
│   └── ai_controller.py
└── tests/
    └── test_reconciliation.py
```
