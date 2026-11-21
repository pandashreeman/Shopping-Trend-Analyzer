import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.visualization import (
    create_bar_chart,
    create_pie_chart
)

from database.db import get_transactions


def show_customer_analysis():

    st.title("👥 Customer Analysis")

    st.write(
        "Understand customer demographics and shopping behaviour."
    )

    st.markdown("---")

    # Load transaction data
    df = get_transactions()

    if df.empty:

        st.warning(
            "No transaction data available. "
            "Please add some shopping transactions first."
        )

        return

    # Customer Overview
    st.subheader("Customer Overview")

    total_customers = df["customer_id"].nunique()

    average_age = df["age"].mean()

    total_purchases = len(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Customers",
            total_customers
        )

    with col2:
        st.metric(
            "Average Customer Age",
            f"{average_age:.1f} years"
        )

    with col3:
        st.metric(
            "Total Purchases",
            total_purchases
        )

    st.markdown("---")

    # Gender Analysis
    st.subheader("Gender Distribution")

    gender_data = df["gender"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(7, 5))

    create_pie_chart(
        ax1,
        gender_data.index,
        gender_data.values,
        "Customers by Gender"
    )

    plt.tight_layout()

    st.pyplot(fig1)

    plt.close(fig1)

    st.markdown("---")

    # Age Analysis
    st.subheader("Customer Age Analysis")

    age_data = df.drop_duplicates(
        subset=["customer_id"]
    ).copy()

    age_data["Age Group"] = pd.cut(
        age_data["age"],
        bins=[0, 18, 30, 45, 60, 100],
        labels=[
            "Below 18",
            "18-30",
            "31-45",
            "46-60",
            "Above 60"
        ]
    )

    age_counts = age_data["Age Group"].value_counts(
        sort=False
    )

    fig2, ax2 = plt.subplots(figsize=(9, 5))

    create_bar_chart(
        ax2,
        age_counts.index.astype(str),
        age_counts.values,
        "Customers by Age Group",
        "Age Group",
        "Number of Customers"
    )

    plt.xticks(rotation=0)

    plt.tight_layout()

    st.pyplot(fig2)

    plt.close(fig2)

    st.markdown("---")

    # Customer Purchase Summary
    st.subheader("Customer Purchase Summary")

    customer_summary = df.groupby(
        ["customer_id", "customer_name"]
    ).agg(
        Total_Purchases=("transaction_id", "count"),
        Total_Spending=("purchase_amount", "sum")
    ).reset_index()

    customer_summary = customer_summary.sort_values(
        by="Total_Spending",
        ascending=False
    )

    # Top Spending Customers
    st.markdown("---")

    st.subheader("🏆 Top 10 Spending Customers")

    top_customers = customer_summary.head(10).copy()

    if not top_customers.empty:

        fig3, ax3 = plt.subplots(figsize=(10, 5))

        ax3.barh(
            top_customers["customer_name"].astype(str),
            top_customers["Total_Spending"],
            color="#800F3F",
            edgecolor="#F4B6CC"
        )

        ax3.set_title(
            "Top 10 Customers by Spending",
            fontsize=14,
            fontweight="bold",
            color="#4A1028"
        )

        ax3.set_xlabel("Total Spending (₹)")
        ax3.set_ylabel("Customer Name")

        ax3.invert_yaxis()

        ax3.set_facecolor("white")

        ax3.tick_params(colors="#4A1028")

        ax3.spines["top"].set_visible(False)
        ax3.spines["right"].set_visible(False)

        ax3.grid(
            axis="x",
            linestyle="--",
            alpha=0.3
        )

        plt.tight_layout()

        st.pyplot(fig3)

        plt.close(fig3)

        # Customer Spending Table
        st.subheader("Customer Spending Details")

        st.dataframe(
            top_customers,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No customer spending information available."
        )

    # Customer Segmentation
    st.markdown("---")

    st.subheader("🎯 Customer Segmentation")

    # Calculate average customer spending
    average_spending = customer_summary[
        "Total_Spending"
    ].mean()

    # Create customer segments
    def assign_segment(spending):

        if spending >= average_spending * 2:
            return "High Value"

        elif spending >= average_spending:
            return "Medium Value"

        else:
            return "Low Value"

    customer_summary["Customer Segment"] = (
        customer_summary["Total_Spending"].apply(
            assign_segment
        )
    )

    # Count customers in each segment
    segment_counts = customer_summary[
        "Customer Segment"
    ].value_counts()

    # Display segment metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "High Value Customers",
            segment_counts.get("High Value", 0)
        )

    with col2:
        st.metric(
            "Medium Value Customers",
            segment_counts.get("Medium Value", 0)
        )

    with col3:
        st.metric(
            "Low Value Customers",
            segment_counts.get("Low Value", 0)
        )

    # Segmentation Chart
    fig4, ax4 = plt.subplots(figsize=(8, 5))

    create_bar_chart(
        ax4,
        segment_counts.index.astype(str),
        segment_counts.values,
        "Customer Segmentation",
        "Customer Segment",
        "Number of Customers"
    )

    plt.xticks(rotation=0)

    plt.tight_layout()

    st.pyplot(fig4)

    plt.close(fig4)

    # Customer Segmentation Table
    st.subheader("Customer Segment Details")

    st.dataframe(
        customer_summary,
        use_container_width=True,
        hide_index=True
    )

    # Customer Purchase History
    st.markdown("---")

    st.subheader("🧾 Customer Purchase History")

    # Get unique customers
    customer_options = df[
        ["customer_id", "customer_name"]
    ].drop_duplicates()

    # Create customer display names
    customer_options["Display"] = (
        customer_options["customer_name"].astype(str)
        + " ("
        + customer_options["customer_id"].astype(str)
        + ")"
    )

    # Select customer
    selected_customer = st.selectbox(
        "Select a Customer",
        customer_options["Display"].tolist()
    )

    # Get selected customer ID
    selected_row = customer_options[
        customer_options["Display"] == selected_customer
    ].iloc[0]

    customer_id = selected_row["customer_id"]

    # Filter customer transactions
    customer_history = df[
        df["customer_id"] == customer_id
    ].copy()

    # Display customer statistics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Purchases",
            len(customer_history)
        )

    with col2:

        total_spending = customer_history[
            "purchase_amount"
        ].sum()

        st.metric(
            "Total Spending",
            f"₹{total_spending:,.2f}"
        )

    # Display purchase history
    st.subheader("Purchase Details")

    st.dataframe(
        customer_history[
            [
                "transaction_id",
                "product",
                "category",
                "quantity",
                "purchase_amount",
                "payment_method",
                "purchase_date"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )