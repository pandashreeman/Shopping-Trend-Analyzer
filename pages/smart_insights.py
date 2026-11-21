import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.db import get_transactions
from utils.visualization import create_bar_chart, create_line_chart


def show_smart_insights():

    st.title("🤖 Smart Shopping Insights")

    st.write(
        "Discover useful shopping trends and "
        "business recommendations using transaction data."
    )

    st.markdown("---")

    # Get transaction data
    df = get_transactions()

    if df.empty:
        st.warning(
            "No transaction data available. "
            "Please add some transactions first."
        )
        return

    # Calculate basic statistics
    total_revenue = df["purchase_amount"].sum()
    total_transactions = len(df)
    total_customers = df["customer_id"].nunique()
    total_products = df["product"].nunique()

    # Business Overview
    st.subheader("📊 Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Revenue", f"₹{total_revenue:,.2f}")

    with col2:
        st.metric("Transactions", total_transactions)

    with col3:
        st.metric("Customers", total_customers)

    with col4:
        st.metric("Products", total_products)

    st.markdown("---")

    # Automatic Business Insights
    st.subheader("💡 Automatic Business Insights")

    # Best Selling Product
    product_sales = df.groupby("product")["quantity"].sum()

    best_product = product_sales.idxmax()
    best_quantity = product_sales.max()

    st.success(
        f"🏆 Best-Selling Product: {best_product} "
        f"with {best_quantity} units sold."
    )

    # Highest Revenue Category
    category_sales = df.groupby("category")[
        "purchase_amount"
    ].sum()

    best_category = category_sales.idxmax()
    best_category_revenue = category_sales.max()

    st.info(
        f"📂 Top Revenue Category: {best_category} "
        f"with revenue of ₹{best_category_revenue:,.2f}."
    )

    # Average Transaction Value
    average_order = total_revenue / total_transactions

    st.info(
        f"💰 Average Transaction Value: ₹{average_order:,.2f}."
    )

    # Best Selling Products Chart
    st.subheader("🏆 Best-Selling Products")

    top_products = product_sales.sort_values(
        ascending=False
    ).head(10).sort_values()

    fig1, ax1 = plt.subplots(figsize=(10, 5))

    create_bar_chart(
        ax1,
        top_products.index,
        top_products.values,
        "Top 10 Products by Quantity Sold",
        "Products",
        "Quantity Sold"
    )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig1)
    plt.close(fig1)

    # Category Revenue Chart
    st.subheader("📂 Revenue by Category")

    fig2, ax2 = plt.subplots(figsize=(9, 5))

    category_chart = category_sales.sort_values(
        ascending=False
    )

    create_bar_chart(
        ax2,
        category_chart.index,
        category_chart.values,
        "Category-wise Revenue",
        "Categories",
        "Revenue (₹)"
    )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig2)
    plt.close(fig2)

    st.markdown("---")

    # Low-Selling Product Analysis
    st.subheader("📉 Low-Selling Products")

    average_quantity = product_sales.mean()

    low_selling_products = product_sales[
        product_sales < average_quantity
    ].sort_values(ascending=True)

    if not low_selling_products.empty:

        st.warning(
            f"Found {len(low_selling_products)} products "
            "with below-average sales."
        )

        low_products_df = low_selling_products.reset_index()

        low_products_df.columns = [
            "Product",
            "Quantity Sold"
        ]

        st.dataframe(
            low_products_df,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Business Recommendation: Consider offering "
            "discounts or promotions for these products "
            "to improve their sales."
        )

    else:
        st.success(
            "All products have sales equal to or above "
            "the average quantity."
        )

    st.markdown("---")

    # Customer Shopping Behaviour
    st.subheader("👥 Customer Shopping Behaviour")

    customer_analysis = df.groupby(
        ["customer_id", "customer_name"]
    ).agg(
        Total_Purchases=("transaction_id", "count"),
        Total_Spending=("purchase_amount", "sum")
    ).reset_index()

    repeat_customers = customer_analysis[
        customer_analysis["Total_Purchases"] > 1
    ]

    average_customer_spending = (
        customer_analysis["Total_Spending"].mean()
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Customers",
            len(customer_analysis)
        )

    with col2:
        st.metric(
            "Repeat Customers",
            len(repeat_customers)
        )

    with col3:
        st.metric(
            "Average Customer Spending",
            f"₹{average_customer_spending:,.2f}"
        )

    # Top Spending Customer
    top_customer = customer_analysis.sort_values(
        by="Total_Spending",
        ascending=False
    ).iloc[0]

    st.success(
        f"🏆 Highest Spending Customer: "
        f"{top_customer['customer_name']} "
        f"with spending of ₹{top_customer['Total_Spending']:,.2f}."
    )

    # Top Customers Chart
    st.subheader("💎 Top Spending Customers")

    top_customers = customer_analysis.sort_values(
        by="Total_Spending",
        ascending=False
    ).head(10).sort_values(by="Total_Spending")

    fig3, ax3 = plt.subplots(figsize=(10, 5))

    create_bar_chart(
        ax3,
        top_customers["customer_name"],
        top_customers["Total_Spending"],
        "Top 10 Customers by Spending",
        "Customers",
        "Total Spending (₹)"
    )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig3)
    plt.close(fig3)

    if len(repeat_customers) > 0:
        st.info(
            "Business Recommendation: Reward repeat customers "
            "with loyalty points, special discounts, or "
            "membership benefits."
        )
    else:
        st.warning(
            "Business Recommendation: Introduce loyalty "
            "offers to encourage customers to purchase again."
        )

    st.markdown("---")

    # Revenue Trend Analysis
    st.subheader("📈 Revenue Trend Insights")

    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"],
        errors="coerce"
    )

    trend_data = df.dropna(
        subset=["purchase_date"]
    ).copy()

    if not trend_data.empty:

        trend_data["Month"] = (
            trend_data["purchase_date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_revenue = trend_data.groupby(
            "Month"
        )["purchase_amount"].sum().sort_index()

        # Monthly Revenue Chart
        fig4, ax4 = plt.subplots(figsize=(10, 5))

        create_line_chart(
            ax4,
            monthly_revenue.index,
            monthly_revenue.values,
            "Monthly Revenue Trend",
            "Month",
            "Revenue (₹)"
        )

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig4)
        plt.close(fig4)

        if len(monthly_revenue) >= 2:

            previous_revenue = monthly_revenue.iloc[-2]
            current_revenue = monthly_revenue.iloc[-1]

            if previous_revenue > 0:

                growth = (
                    (current_revenue - previous_revenue)
                    / previous_revenue
                ) * 100

                if growth > 0:
                    st.success(
                        f"📈 Revenue increased by {growth:.2f}% "
                        "compared to the previous month."
                    )

                elif growth < 0:
                    st.warning(
                        f"📉 Revenue decreased by {abs(growth):.2f}% "
                        "compared to the previous month."
                    )

                else:
                    st.info(
                        "Revenue remained unchanged compared "
                        "to the previous month."
                    )

            else:
                st.info(
                    "Previous month's revenue was zero. "
                    "Growth percentage cannot be calculated."
                )

        else:
            st.info(
                "At least two months of sales data are needed "
                "to calculate revenue growth."
            )

    else:
        st.warning("No valid purchase dates available.")

    st.markdown("---")

    # Automatic Business Recommendations
    st.subheader("💡 Smart Business Recommendations")

    repeat_percentage = (
        len(repeat_customers) / len(customer_analysis)
    ) * 100

    st.markdown("### 📌 Recommendations")

    st.success(
        f"🏆 **Promote Best-Selling Product:** "
        f"{best_product} is your best-selling product. "
        "Consider maintaining sufficient stock."
    )

    st.info(
        f"📂 **Focus on Top Category:** "
        f"{best_category} generates the highest revenue. "
        "Consider expanding products in this category."
    )

    if not low_selling_products.empty:
        st.warning(
            "📉 **Improve Low-Selling Products:** "
            "Consider discounts and promotional offers "
            "to increase sales."
        )

    st.info(
        f"👥 **Customer Retention:** "
        f"{repeat_percentage:.2f}% of customers are repeat customers. "
        "Introduce loyalty rewards to encourage repeat purchases."
    )

    st.markdown("---")

    st.caption(
        "These recommendations are generated automatically "
        "using the available shopping transaction data."
    )