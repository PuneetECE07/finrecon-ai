import pandas as pd
from src.reconciliation import reconcile

def test_exact_match():
    tx = pd.DataFrame([{
        "transaction_id": "TXN1", "amount": 1000,
        "transaction_date": "2026-08-01", "customer": "A", "status": "SUCCESS"
    }])
    se = pd.DataFrame([{
        "transaction_id": "TXN1", "settlement_amount": 1000,
        "settlement_date": "2026-08-02"
    }])
    ba = pd.DataFrame([{
        "transaction_id": "TXN1", "bank_amount": 1000,
        "bank_date": "2026-08-02", "bank_reference": "B1"
    }])

    result = reconcile(tx, se, ba)
    assert result["matched"] == 1
    assert result["match_rate"] == 100.0

def test_missing_settlement():
    tx = pd.DataFrame([{
        "transaction_id": "TXN1", "amount": 1000,
        "transaction_date": "2026-08-01", "customer": "A", "status": "SUCCESS"
    }])
    se = pd.DataFrame(columns=["transaction_id", "settlement_amount", "settlement_date"])
    ba = pd.DataFrame([{
        "transaction_id": "TXN1", "bank_amount": 1000,
        "bank_date": "2026-08-02", "bank_reference": "B1"
    }])

    result = reconcile(tx, se, ba)
    assert result["exceptions"] == 1
    assert result["results"].iloc[0]["exception_reason"] == "Missing settlement record"
