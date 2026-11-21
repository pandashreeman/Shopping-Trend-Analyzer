import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.db import get_transactions
from utils.visualization import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart
)


def show_sales_analysis():

    st.title("💰 Sales Analysis")

    st.write(
        "Analyze sales performance, revenue trends, "
        "and payment methods."
    )

    st.markdown("---")

    # Get transaction data
    df = get_transactions()

    if df.empty:
        st.warning(
            "No sales data available. "
            "Please add some transactions first."
        )
        return

    # Convert purchase date
    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"],
        errors="coerce"
    )

    df = df.dropna(subset=["purchase_date"])

    if df.empty:
        st.warning("No valid sales dates are available.")
        return

    # Sales Overview
    st.subheader("📊 Sales Overview")

    total_revenue = df["purchase_amount"].sum()
    total_transactions = len(df)

    average_order_value = (
        total_revenue / total_transactions
        if total_transactions > 0 else 0
    )

    total_units = df["quantity"].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Revenue", f"₹{total_revenue:,.2f}")

    with col2:
        st.metric("Total Transactions", total_transactions)

    with col3:
        st.metric("Average Order Value", f"₹{average_order_value:,.2f}")

    with col4:
        st.metric("Total Units Sold", int(total_units))

    st.markdown("---")

    # Sales Data Table
    st.subheader("📋 Sales Records")

    st.dataframe(
        df[
            [
                "transaction_id",
                "customer_name",
                "product",
                "quantity",
                "purchase_amount",
                "payment_method",
                "purchase_date"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Daily Sales Analysis
    st.subheader("📅 Daily Sales Analysis")

    daily_sales = df.groupby(
        df["purchase_date"].dt.date
    ).agg(
        Total_Revenue=("purchase_amount", "sum"),
        Total_Transactions=("transaction_id", "count")
    ).reset_index()

    daily_sales.columns = [
        "Purchase Date",
        "Total Revenue",
        "Total Transactions"
    ]

    daily_sales = daily_sales.sort_values(
        by="Purchase Date"
    )

    # Daily Revenue Chart
    fig1, ax1 = plt.subplots(figsize=(10, 5))

    create_line_chart(
        ax1,
        daily_sales["Purchase Date"],
        daily_sales["Total Revenue"],
        "Daily Revenue Trend",
        "Purchase Date",
        "Revenue (₹)"
    )

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig1)
    plt.close(fig1)

    # Daily Sales Details
    st.subheader("Daily Sales Details")

    st.dataframe(
        daily_sales,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Monthly Sales Analysis
    st.subheader("📆 Monthly Sales Analysis")

    monthly_sales = df.copy()

    monthly_sales["Month"] = (
        monthly_sales["purchase_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_summary = monthly_sales.groupby("Month").agg(
        Total_Revenue=("purchase_amount", "sum"),
        Total_Transactions=("transaction_id", "count")
    ).reset_index()

    monthly_summary = monthly_summary.sort_values(
        by="Month"
    )

    # Monthly Revenue Chart
    fig2, ax2 = plt.subplots(figsize=(10, 5))

    create_bar_chart(
        ax2,
        monthly_summary["Month"],
        monthly_summary["Total_Revenue"],
        "Monthly Revenue Analysis",
        "Month",
        "Revenue (₹)"
    )

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)
    plt.close(fig2)

    # Monthly Sales Details
    st.subheader("Monthly Sales Details")

    st.dataframe(
        monthly_summary,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Payment Method Analysis
    st.subheader("💳 Payment Method Analysis")

    payment_summary = df.groupby("payment_method").agg(
        Total_Transactions=("transaction_id", "count"),
        Total_Revenue=("purchase_amount", "sum")
    ).reset_index()

    payment_summary = payment_summary.sort_values(
        by="Total_Transactions",
        ascending=False
    )

    # Payment Method Chart
    fig3, ax3 = plt.subplots(figsize=(8, 5))

    create_pie_chart(
        ax3,
        payment_summary["payment_method"],
        payment_summary["Total_Transactions"],
        "Transactions by Payment Method"
    )

    st.pyplot(fig3)
    plt.close(fig3)

    # Payment Details
    st.subheader("Payment Method Details")

    st.dataframe(
        payment_summary,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Sales Performance Summary
    st.subheader("🏆 Sales Performance Summary")

    best_day = daily_sales.loc[
        daily_sales["Total Revenue"].idxmax()
    ]

    best_month = monthly_summary.loc[
        monthly_summary["Total_Revenue"].idxmax()
    ]

    popular_payment = payment_summary.loc[
        payment_summary["Total_Transactions"].idxmax()
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Best Sales Day",
            str(best_day["Purchase Date"]),
            f"₹{best_day['Total Revenue']:,.2f}"
        )

    with col2:
        st.metric(
            "Best Sales Month",
            best_month["Month"],
            f"₹{best_month['Total_Revenue']:,.2f}"
        )

    with col3:
        st.metric(
            "Popular Payment Method",
            str(popular_payment["payment_method"]),
            f"{popular_payment['Total_Transactions']} transactions"
        )