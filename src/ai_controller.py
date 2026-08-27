import os

def explain_exception(row: dict) -> str:
    """
    Uses an LLM when OPENAI_API_KEY is available.
    Otherwise provides a deterministic explanation so the demo still works.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            prompt = f"""
You are a finance reconciliation analyst.
Explain this synthetic transaction exception clearly and conservatively.
Do not invent facts. State what is known, what the discrepancy is,
and what a finance operator should verify.

Transaction ID: {row.get("transaction_id")}
Transaction amount: {row.get("amount")}
Settlement amount: {row.get("settlement_amount")}
Bank amount: {row.get("bank_amount")}
Reason: {row.get("exception_reason")}
Difference: {row.get("difference")}
"""

            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                input=prompt
            )
            return response.output_text
        except Exception:
            pass

    reason = row.get("exception_reason", "Unknown exception")
    txn = row.get("transaction_id", "Unknown")
    amount = row.get("amount", "N/A")
    settlement = row.get("settlement_amount", "N/A")
    bank = row.get("bank_amount", "N/A")
    diff = row.get("difference", "N/A")

    if reason == "Missing settlement record":
        action = "Verify whether the payment has entered the settlement cycle."
    elif reason == "Missing bank record":
        action = "Verify the bank statement/import and settlement payout reference."
    elif reason == "Duplicate bank records detected":
        action = "Check whether one bank entry is duplicated before posting or closing."
    elif reason == "Settlement amount mismatch":
        action = "Verify fees, refunds, adjustments, or settlement deductions."
    elif reason == "Bank amount mismatch":
        action = "Verify bank fees, adjustments, or incorrect statement data."
    else:
        action = "Review the source records manually."

    return (
        f"{txn} is flagged because: {reason}. "
        f"Transaction amount is ₹{amount}; settlement is ₹{settlement}; "
        f"bank amount is ₹{bank}. Difference: {diff}. "
        f"Recommended action: {action}"
    )
