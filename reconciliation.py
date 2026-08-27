import pandas as pd

def reconcile(transactions: pd.DataFrame,
              settlements: pd.DataFrame,
              bank_records: pd.DataFrame) -> dict:
    tx = transactions.copy()
    se = settlements.copy()
    ba = bank_records.copy()

    # Detect duplicate bank records before merging.
    bank_counts = ba.groupby("transaction_id").size().rename("bank_record_count")
    ba = ba.merge(bank_counts, on="transaction_id", how="left")

    # Aggregate duplicate bank rows so one transaction remains one result row.
    bank_agg = (
        ba.groupby("transaction_id", as_index=False)
        .agg(
            bank_amount=("bank_amount", "sum"),
            bank_record_count=("bank_record_count", "max"),
            bank_reference=("bank_reference", "first"),
            bank_date=("bank_date", "first")
        )
    )

    merged = tx.merge(
        se[["transaction_id", "settlement_amount", "settlement_date"]],
        on="transaction_id", how="left"
    ).merge(
        bank_agg[["transaction_id", "bank_amount", "bank_record_count",
                  "bank_reference", "bank_date"]],
        on="transaction_id", how="left"
    )

    statuses = []
    reasons = []
    differences = []

    for _, r in merged.iterrows():
        amount = float(r["amount"])
        settlement = r["settlement_amount"]
        bank = r["bank_amount"]
        duplicate_bank = (
            pd.notna(r["bank_record_count"]) and int(r["bank_record_count"]) > 1
        )

        if pd.isna(settlement):
            status, reason = "EXCEPTION", "Missing settlement record"
            diff = None
        elif pd.isna(bank):
            status, reason = "EXCEPTION", "Missing bank record"
            diff = None
        elif duplicate_bank:
            status, reason = "EXCEPTION", "Duplicate bank records detected"
            diff = float(bank) - amount
        elif float(settlement) != amount:
            status, reason = "EXCEPTION", "Settlement amount mismatch"
            diff = float(settlement) - amount
        elif float(bank) != amount:
            status, reason = "EXCEPTION", "Bank amount mismatch"
            diff = float(bank) - amount
        else:
            status, reason = "MATCHED", "Payment, settlement and bank amounts match"
            diff = 0.0

        statuses.append(status)
        reasons.append(reason)
        differences.append(diff)

    merged["status"] = statuses
    merged["exception_reason"] = reasons
    merged["difference"] = differences

    total = len(merged)
    matched = int((merged["status"] == "MATCHED").sum())
    exceptions = total - matched
    match_rate = (matched / total * 100) if total else 0.0

    breakdown = (
        merged[merged["status"] == "EXCEPTION"]["exception_reason"]
        .value_counts()
        .rename_axis("exception")
        .to_frame("count")
    )

    return {
        "results": merged,
        "total": total,
        "matched": matched,
        "exceptions": exceptions,
        "match_rate": match_rate,
        "exception_breakdown": breakdown,
    }
