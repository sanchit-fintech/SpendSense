import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SpendSense",
    page_icon="💰",
    layout="wide"
)
# -----------------------------
# CUSTOM UI
# -----------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    letter-spacing: -2px;
}

h2, h3 {
    font-weight: 700 !important;
}

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 18px;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-weight: 700;
    padding: 0.7rem;
}

.stTextInput > div > div,
.stNumberInput > div > div,
.stSelectbox > div > div {
    border-radius: 12px;
}

</style>
""")

st.title("💰 SpendSense")
st.subheader("Your Smart Student Expense Tracker")
st.write("Track your expenses. Control your spending. Save smarter. 🚀")

st.divider()

# -----------------------------
# MONTHLY BUDGET
# -----------------------------

budget = st.number_input(
    "Monthly Budget (₹)",
    min_value=0,
    value=5000,
    step=500
)

st.divider()

# -----------------------------
# ADD EXPENSE
# -----------------------------

st.header("➕ Add an Expense")

col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input(
        "Amount (₹)",
        min_value=0,
        value=0,
        step=10
    )

with col2:
    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Entertainment",
            "Bills",
            "Education",
            "Other"
        ]
    )

with col3:
    description = st.text_input(
        "Description",
        placeholder="e.g. Lunch at college"
    )

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if st.button("Add Expense"):
    if amount > 0:
        st.session_state.expenses.append(
            {
                "Amount": amount,
                "Category": category,
                "Description": description
            }
        )
        st.success("Expense added successfully! ✅")
    else:
        st.warning("Enter an amount greater than ₹0.")

st.divider()

# -----------------------------
# DASHBOARD
# -----------------------------

st.header("📊 Spending Dashboard")

if st.session_state.expenses:

    df = pd.DataFrame(st.session_state.expenses)

    total_spent = df["Amount"].sum()
    remaining = budget - total_spent

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💸 Total Spent", f"₹{total_spent:,.0f}")

    with col2:
        st.metric("💰 Remaining", f"₹{remaining:,.0f}")

    with col3:
        st.metric("🧾 Transactions", len(df))

    st.subheader("Expense History")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Spending by Category")

    category_data = df.groupby("Category")["Amount"].sum().reset_index()

    fig = px.pie(
        category_data,
        names="Category",
        values="Amount",
        title="Where Your Money Is Going"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("No expenses added yet. Start by adding your first expense above! 👆")