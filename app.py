import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
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
# DATABASE
# --------------------------------------------------

DB_NAME = "spendsense.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def setup_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(amount, category, description, expense_date):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO expenses
        (amount, category, description, expense_date)
        VALUES (?, ?, ?, ?)
        """,
        (
            amount,
            category,
            description,
            str(expense_date)
        )
    )

    conn.commit()
    conn.close()


def load_expenses():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            amount AS Amount,
            category AS Category,
            description AS Description,
            expense_date AS Date
        FROM expenses
        ORDER BY expense_date DESC
        """,
        conn
    )

    conn.close()

    return df


def delete_expense(expense_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()


setup_database()

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

.card {
    padding: 1.35rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
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

.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
}

</style>
""", unsafe_allow_html=True)

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

st.subheader("🎯 Monthly Budget")

budget = st.number_input(
    "How much money are you working with this month?",
    min_value=0,
    value=5000,
    step=500
)

# --------------------------------------------------
# LOAD EXPENSES
# --------------------------------------------------

df = load_expenses()

total_spent = df["Amount"].sum() if not df.empty else 0
remaining = budget - total_spent
transactions = len(df)

if budget > 0:
    budget_used = min(total_spent / budget, 1)
    percentage_used = (total_spent / budget) * 100
else:
    budget_used = 0
    percentage_used = 0

# --------------------------------------------------
# DASHBOARD
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
# BUDGET HEALTH
# --------------------------------------------------

st.write("")
st.subheader("🔋 Budget Health")

st.progress(budget_used)

if budget > 0:

    if percentage_used < 50:
        st.success(
            f"You're using {percentage_used:.1f}% of your budget. "
            "You're doing great 🔥"
        )

    elif percentage_used < 80:
        st.info(
            f"You've used {percentage_used:.1f}% of your budget. "
            "Keep an eye on those small expenses 👀"
        )

    elif percentage_used < 100:
        st.warning(
            f"You've used {percentage_used:.1f}% of your budget. "
            "Careful now 😭"
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

        add_expense(
            amount,
            category,
            description,
            expense_date
        )

        st.success("Expense saved permanently! 💾")

        st.rerun()

    else:

        st.warning("Enter an amount first.")

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

if not df.empty:

    st.write("")
    st.subheader("🧠 Quick Insight")

    category_totals = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_totals.index[0]
    top_amount = category_totals.iloc[0]

    st.info(
        f"👀 Your biggest spending category is "
        f"**{top_category}** at **₹{top_amount:,.0f}**."
    )

    # --------------------------------------------------
    # CHART
    # --------------------------------------------------

    st.subheader("🍕 Where Is Your Money Going?")

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

    # --------------------------------------------------
    # EXPENSE HISTORY
    # --------------------------------------------------

    st.subheader("🧾 Expense History")

    st.dataframe(
        df.drop(columns=["id"]),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # DELETE EXPENSE
    # --------------------------------------------------

    st.subheader("🗑️ Delete an Expense")

    expense_options = {
        f"₹{row.Amount:.0f} — {row.Description or row.Category} ({row.Date})":
        row.id
        for _, row in df.iterrows()
    }

    selected_expense = st.selectbox(
        "Select an expense",
        list(expense_options.keys())
    )

    if st.button("Delete Selected Expense"):

        delete_expense(
            expense_options[selected_expense]
        )

        st.success("Expense deleted.")

        st.rerun()

else:

    st.info(
        "👀 Your wallet is currently mysterious. "
        "Add your first expense and let's see where your money disappears."
    )