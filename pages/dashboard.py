import streamlit as st
from database.db import get_transactions


def show_dashboard():

    username = st.session_state.user["username"]

    # Professional Dashboard Header
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(120deg, #4A1028, #800F3F);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
        ">
            <h1 style="color: #FCE7EF; margin-bottom: 8px;">
                Welcome Back, {username}! 👋
            </h1>
            <p style="color: #F4B6CC; font-size: 17px; margin-bottom: 0;">Your Shopping Trend Analyzer Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Get latest transaction data
    df = get_transactions()

    # Calculate statistics
    total_transactions = len(df)

    if not df.empty:

        total_revenue = df["purchase_amount"].sum()

        total_customers = df["customer_id"].nunique()

        total_products = df["product"].nunique()

    else:

        total_revenue = 0
        total_customers = 0
        total_products = 0

    # Dashboard Statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🛒 Total Transactions",
            value=f"{total_transactions:,}"
        )

    with col2:
        st.metric(
            label="💰 Total Revenue",
            value=f"₹{total_revenue:,.2f}"
        )

    with col3:
        st.metric(
            label="👥 Total Customers",
            value=f"{total_customers:,}"
        )

    with col4:
        st.metric(
            label="📦 Total Products",
            value=f"{total_products:,}"
        )

    st.markdown("---")

    # Recent Activity
    left, right = st.columns(2)

    with left:

        st.markdown("### Recent Transactions")

        if not df.empty:

            st.dataframe(
                df[
                    [
                        "transaction_id",
                        "customer_name",
                        "product",
                        "purchase_amount"
                    ]
                ].head(5),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No recent transactions available."
            )

    with right:

        st.markdown("### Quick Access")

        st.markdown("""
        - 📁 Dataset Management
        - ➕ Add Shopping Transaction
        - 📋 View Transactions
        - 📊 Customer Analysis
        - 🛍️ Product Analysis
        - 💰 Sales Analysis
        - 💡 Smart Insights
        - 📄 Reports
        """)

    st.markdown("---")

    st.markdown(
        "<center>Shopping Trend Analyzer | BCA Minor Project</center>",
        unsafe_allow_html=True
    )