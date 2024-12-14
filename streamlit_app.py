import streamlit as st
import pandas as pd

# Initialize session state to store profits and balance
if "daily_profits" not in st.session_state:
    st.session_state.daily_profits = []
if "withdrawn" not in st.session_state:
    st.session_state.withdrawn = 0
if "account_balance" not in st.session_state:
    st.session_state.account_balance = 10000

# App title
st.title("Consistency Rule Tracker")

# Input for daily profit
st.header("Add/Remove Daily Profit")
daily_profit = st.number_input("Enter today's profit ($):", min_value=0.0, step=0.01)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Add Profit"):
        st.session_state.daily_profits.append(float(daily_profit))
        st.success(f"Added ${daily_profit} to daily profits!")
        
with col2:
    if st.button("Remove Last Profit"):
        if st.session_state.daily_profits:
            removed_profit = st.session_state.daily_profits.pop()
            st.warning(f"Removed the last entered profit: ${removed_profit}")
        else:
            st.warning("No profits to remove.")

with col3:
    if st.button("Clear All"):
        st.session_state.daily_profits = []
        st.session_state.withdrawn = 0
        st.session_state.account_balance = 10000
        st.success("All inputs cleared! You can start afresh.")

# Calculate metrics
total_profit = sum(st.session_state.daily_profits)
best_day_profit = max(st.session_state.daily_profits) if st.session_state.daily_profits else 0
pnl_percentage = (best_day_profit / total_profit * 100) if total_profit > 0 else 0

# Check withdrawal eligibility
withdrawable_amount = min(750, total_profit - st.session_state.withdrawn)
eligible_for_withdrawal = pnl_percentage <= 40 and withdrawable_amount >= 500

# Display metrics
st.header("Account Summary")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Best Day Profit", f"${best_day_profit:,.2f}")
st.metric("P&L % (Best Day)", f"{pnl_percentage:.2f}%")
st.metric("Withdrawable Amount", f"${withdrawable_amount:,.2f}")

# Withdrawal section
st.header("Withdrawal")
if eligible_for_withdrawal:
    st.success("🎉 You are eligible for a withdrawal!")
    withdrawal_request = st.number_input(
        "Enter withdrawal amount ($):",
        min_value=500.0,
        max_value=float(withdrawable_amount),  # Constrain between $500 and withdrawable_amount
        step=0.01,
    )
    if st.button("Submit Withdrawal"):
        if withdrawal_request >= 500:
            st.session_state.withdrawn += withdrawal_request
            st.session_state.account_balance -= withdrawal_request
            st.success(f"Successfully withdrawn ${withdrawal_request}!")
        else:
            st.error("Withdrawal must be at least $500.")
else:
    st.warning("Not eligible for withdrawal. Ensure the P&L % is ≤ 40% and you have at least $500 withdrawable.")

# Notify when P&L% drops below 40%
if not eligible_for_withdrawal and pnl_percentage > 40:
    st.info(f"⚠️ To be eligible for withdrawal, ensure the best day's profit is ≤ 40% of total profit. Current P&L%: {pnl_percentage:.2f}%.")

# Display profit history
st.header("Daily Profit History")
if st.session_state.daily_profits:
    df = pd.DataFrame({"Day": range(1, len(st.session_state.daily_profits) + 1), "Profit ($)": st.session_state.daily_profits})
    st.line_chart(df.set_index("Day"))
    st.write(df)
else:
    st.write("No profits recorded yet.")
