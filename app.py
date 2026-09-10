import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="SpendSense",
    page_icon="💸",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM UI
# --------------------------------------------------

st.markdown("""
<style>

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Hero */
.hero {
    padding: 2.2rem 2rem;
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        rgba(120, 80, 255, 0.22),
        rgba(0, 190, 255, 0.12)
    );
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 850;
    letter-spacing: -2px;
    margin-bottom: 0.3rem;
}

.hero-text {
    font-size: 1.1rem;
    opacity: 0.72;
}

/* Cards */
.card {
    padding: 1.35rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
}

.card-title {
    font-size: 0.9rem;
    opacity: 0.65;
}

.card-value {
    font-size: 2rem;
    font-weight: 800;
    margin-top: 0.4rem;
}

/* Section boxes */
.section-box {
    padding: 1.5rem;
    border-radius: 22px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

/* Inputs */
input, textarea {
    border-radius: 12px !important;
}

/* Progress */
.stProgress > div > div {
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">💸 SpendSense</div>
    <div class="hero-text">
        Your money. Your choices. Your month.
        <br>
        Track smarter. Spend better. 😎
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# BUDGET
# --------------------------------------------------

st.subheader("🎯 Set Your Monthly Budget")

budget = st.number_input(
    "How much money are you working with this month?",
    min_value=0,
    value=5000,
    step=500
)

# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

if st.session_state.expenses:

    df = pd.DataFrame(st.session_state.expenses)

    total_spent = df["Amount"].sum()
    remaining = budget - total_spent
    transactions = len(df)

else:

    df = pd.DataFrame(
        columns=["Amount", "Category", "Description", "Date"]
    )

    total_spent = 0
    remaining = budget
    transactions = 0

if budget > 0:
    budget_used = min(total_spent / budget, 1)
    percentage_used = (total_spent / budget) * 100
else:
    budget_used = 0
    percentage_used = 0

# --------------------------------------------------
# TOP DASHBOARD
# --------------------------------------------------

st.write("")
st.subheader("📊 Your Money Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">💸 Spent</div>
            <div class="card-value">₹{total_spent:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">💰 Remaining</div>
            <div class="card-value">₹{remaining:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">🧾 Transactions</div>
            <div class="card-value">{transactions}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    if percentage_used < 50:
        mood = "😎 Chill"
    elif percentage_used < 80:
        mood = "🙂 Careful"
    elif percentage_used < 100:
        mood = "😬 Uh oh"
    else:
        mood = "💀 BRO"

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">🧠 Spending Mood</div>
            <div class="card-value">{mood}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# BUDGET METER
# --------------------------------------------------

st.write("")
st.markdown(
    f"""
    <div class="section-box">
        <h3>🔋 Budget Health</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.progress(budget_used)

if budget > 0:

    if percentage_used < 50:
        st.success(
            f"You're using {percentage_used:.1f}% of your budget. "
            "You're doing great. Keep it up 🔥"
        )

    elif percentage_used < 80:
        st.info(
            f"You've used {percentage_used:.1f}% of your budget. "
            "Time to keep an eye on those little expenses 👀"
        )

    elif percentage_used < 100:
        st.warning(
            f"You've used {percentage_used:.1f}% of your budget. "
            "The month isn't over yet 😭"
        )

    else:
        st.error(
            f"You've used {percentage_used:.1f}% of your budget. "
            "BRO. PUT THE WALLET DOWN. 💀"
        )

# --------------------------------------------------
# ADD EXPENSE
# --------------------------------------------------

st.write("")
st.subheader("➕ Add an Expense")

col1, col2 = st.columns(2)

with col1:

    amount = st.number_input(
        "💵 Amount",
        min_value=0,
        value=0,
        step=10
    )

    category = st.selectbox(
        "📂 Category",
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

with col2:

    description = st.text_input(
        "📝 What did you spend on?",
        placeholder="e.g. Pizza with friends"
    )

    expense_date = st.date_input(
        "📅 Date",
        value=date.today()
    )

if st.button("Add Expense 🚀"):

    if amount > 0:

        st.session_state.expenses.append(
            {
                "Amount": amount,
                "Category": category,
                "Description": description,
                "Date": expense_date
            }
        )

        st.success("Expense added! 💸")

    else:

        st.warning("Enter an amount first.")

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

if st.session_state.expenses:

    # Refresh dataframe after adding an expense
    df = pd.DataFrame(st.session_state.expenses)

    st.write("")
    st.subheader("🧠 Quick Insight")

    category_totals = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    if not category_totals.empty:

        top_category = category_totals.index[0]
        top_amount = category_totals.iloc[0]

        st.info(
            f"👀 Your biggest spending category right now is "
            f"**{top_category}** at **₹{top_amount:,.0f}**."
        )
    # --------------------------------------------------
    # CHART + RECENT EXPENSES
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("🍕 Where Your Money Goes")

        fig = px.pie(
            category_totals.reset_index(),
            names="Category",
            values="Amount",
            hole=0.5
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("🧾 Recent Expenses")

        recent_df = df.sort_values(
            "Date",
            ascending=False
        ).copy()

        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True
        )

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

else:

    st.write("")
    st.markdown("""
    <div class="section-box">

    ### 👀 Your wallet is currently mysterious.

    Add a few expenses and SpendSense will start figuring out:

    **Where you spend → What you spend on → How fast your budget disappears**

    </div>
    """, unsafe_allow_html=True)