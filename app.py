import os
import pandas as pd
import streamlit as st
from src.reconciliation import reconcile
from src.ai_controller import explain_exception

st.set_page_config(page_title="FinRecon AI", page_icon="💳", layout="wide")

st.title("💳 FinRecon AI")
st.caption("Autonomous Finance Reconciliation Agent")

st.markdown("""
FinRecon AI reconciles payment transactions against settlement and bank records,
detects exceptions, calculates measurable reconciliation metrics, and provides
AI-assisted explanations for finance teams.
""")

@st.cache_data
def load_data():
    tx = pd.read_csv("data/transactions.csv")
    se = pd.read_csv("data/settlements.csv")
    ba = pd.read_csv("data/bank_records.csv")
    return tx, se, ba

tx, se, ba = load_data()
result = reconcile(tx, se, ba)
df = result["results"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Transactions", result["total"])
c2.metric("Matched", result["matched"])
c3.metric("Exceptions", result["exceptions"])
c4.metric("Match Rate", f'{result["match_rate"]:.1f}%')

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("Exception Breakdown")
    if not result["exception_breakdown"].empty:
        st.bar_chart(result["exception_breakdown"])
    else:
        st.info("No exceptions detected.")

with right:
    st.subheader("Reconciliation Summary")
    st.write(
        f'**High-confidence matches:** {result["matched"]}  \n'
        f'**Records requiring review:** {result["exceptions"]}  \n'
        f'**Match rate:** {result["match_rate"]:.1f}%'
    )
    st.download_button(
        "Download reconciliation CSV",
        df.to_csv(index=False).encode("utf-8"),
        "reconciliation_report.csv",
        "text/csv"
    )

st.divider()
st.subheader("Transaction Reconciliation Results")
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("AI Exception Analyst")

exceptions_df = df[df["status"] != "MATCHED"]
if exceptions_df.empty:
    st.success("All transactions matched.")
else:
    selected = st.selectbox(
        "Select an exception",
        exceptions_df["transaction_id"].tolist()
    )
    row = exceptions_df[exceptions_df["transaction_id"] == selected].iloc[0].to_dict()

    if st.button("Analyze with AI"):
        with st.spinner("Analyzing exception..."):
            explanation = explain_exception(row)
        st.info(explanation)

st.caption("Demo data is fully synthetic. No real financial/customer data is used.")
