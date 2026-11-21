import streamlit as st
import pandas as pd
from database.db import get_transactions
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER


# Theme Colors
BURGUNDY = colors.HexColor("#800F3F")
DARK_BURGUNDY = colors.HexColor("#4A1028")
BABY_PINK = colors.HexColor("#FCE7EF")
SOFT_PINK = colors.HexColor("#F4B6CC")
WHITE = colors.white


def show_reports():

    st.title("📊 Reports & Data Export")

    st.write(
        "Generate and download shopping transaction reports."
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

    # Report Overview
    st.subheader("📈 Report Overview")

    total_transactions = len(df)
    total_revenue = df["purchase_amount"].sum()
    total_customers = df["customer_id"].nunique()
    total_products = df["product"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Transactions", total_transactions)

    with col2:
        st.metric("Total Revenue", f"₹{total_revenue:,.2f}")

    with col3:
        st.metric("Customers", total_customers)

    with col4:
        st.metric("Products", total_products)

    st.markdown("---")

    # Transaction Report
    st.subheader("📋 Transaction Report")

    st.write("Preview all available shopping transactions.")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # CSV Report Export
    st.subheader("📥 Download Transaction Report")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Transactions as CSV",
        data=csv_data,
        file_name="shopping_transactions.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # Sales Summary Report
    st.subheader("💰 Sales Summary Report")

    sales_summary = df.groupby("category").agg(
        Total_Transactions=("transaction_id", "count"),
        Total_Quantity=("quantity", "sum"),
        Total_Revenue=("purchase_amount", "sum")
    ).reset_index()

    sales_summary["Average_Revenue"] = (
        sales_summary["Total_Revenue"]
        / sales_summary["Total_Transactions"]
    )

    sales_summary = sales_summary.sort_values(
        by="Total_Revenue",
        ascending=False
    )

    st.dataframe(
        sales_summary,
        use_container_width=True,
        hide_index=True
    )

    sales_csv = sales_summary.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Sales Summary",
        data=sales_csv,
        file_name="sales_summary.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # Customer Report
    st.subheader("👥 Customer Report")

    customer_report = df.groupby(
        ["customer_id", "customer_name"]
    ).agg(
        Total_Purchases=("transaction_id", "count"),
        Total_Quantity=("quantity", "sum"),
        Total_Spending=("purchase_amount", "sum")
    ).reset_index()

    customer_report["Average_Order_Value"] = (
        customer_report["Total_Spending"]
        / customer_report["Total_Purchases"]
    )

    customer_report = customer_report.sort_values(
        by="Total_Spending",
        ascending=False
    )

    st.dataframe(
        customer_report,
        use_container_width=True,
        hide_index=True
    )

    customer_csv = customer_report.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Customer Report",
        data=customer_csv,
        file_name="customer_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # Product Performance Report
    st.subheader("🛍️ Product Performance Report")

    product_report = df.groupby("product").agg(
        Total_Transactions=("transaction_id", "count"),
        Total_Quantity=("quantity", "sum"),
        Total_Revenue=("purchase_amount", "sum")
    ).reset_index()

    product_report = product_report.sort_values(
        by="Total_Revenue",
        ascending=False
    )

    st.dataframe(
        product_report,
        use_container_width=True,
        hide_index=True
    )

    product_csv = product_report.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Product Report",
        data=product_csv,
        file_name="product_performance_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # PDF Report Generation
    st.subheader("📄 Generate PDF Report")

    st.write(
        "Create a professional PDF containing business "
        "statistics, category sales, and top customers."
    )

    if st.button("📄 Generate PDF Report"):

        buffer = BytesIO()

        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            textColor=DARK_BURGUNDY,
            fontSize=22,
            alignment=TA_CENTER,
            spaceAfter=15
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            textColor=BURGUNDY,
            fontSize=15,
            spaceBefore=12,
            spaceAfter=10
        )

        content = []

        # PDF Title
        content.append(
            Paragraph(
                "Shopping Trend Analyzer Report",
                title_style
            )
        )

        content.append(
            Paragraph(
                "Business Performance and Shopping Analysis",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 20))

        # Business Summary
        content.append(
            Paragraph(
                "Business Summary",
                heading_style
            )
        )

        summary_data = [
            ["Metric", "Value"],
            ["Total Transactions", str(total_transactions)],
            ["Total Revenue", f"Rs. {total_revenue:,.2f}"],
            ["Total Customers", str(total_customers)],
            ["Total Products", str(total_products)]
        ]

        summary_table = Table(
            summary_data,
            colWidths=[250, 200]
        )

        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BURGUNDY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("BACKGROUND", (0, 1), (-1, -1), BABY_PINK),
            ("TEXTCOLOR", (0, 1), (-1, -1), DARK_BURGUNDY),
            ("GRID", (0, 0), (-1, -1), 0.5, SOFT_PINK),
            ("PADDING", (0, 0), (-1, -1), 8)
        ]))

        content.append(summary_table)
        content.append(Spacer(1, 20))

        # Category Sales Summary
        content.append(
            Paragraph(
                "Category Sales Summary",
                heading_style
            )
        )

        pdf_category_data = [
            ["Category", "Quantity", "Revenue"]
        ]

        for _, row in sales_summary.iterrows():

            pdf_category_data.append([
                str(row["category"]),
                str(row["Total_Quantity"]),
                f"Rs. {row['Total_Revenue']:,.2f}"
            ])

        category_table = Table(
            pdf_category_data,
            colWidths=[170, 100, 180],
            repeatRows=1
        )

        category_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BURGUNDY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("BACKGROUND", (0, 1), (-1, -1), BABY_PINK),
            ("TEXTCOLOR", (0, 1), (-1, -1), DARK_BURGUNDY),
            ("GRID", (0, 0), (-1, -1), 0.5, SOFT_PINK),
            ("PADDING", (0, 0), (-1, -1), 7)
        ]))

        content.append(category_table)
        content.append(Spacer(1, 20))

        # Top 10 Customers
        content.append(
            Paragraph(
                "Top 10 Customers",
                heading_style
            )
        )

        pdf_customer_data = [
            ["Customer", "Purchases", "Total Spending"]
        ]

        for _, row in customer_report.head(10).iterrows():

            pdf_customer_data.append([
                str(row["customer_name"]),
                str(row["Total_Purchases"]),
                f"Rs. {row['Total_Spending']:,.2f}"
            ])

        customer_table = Table(
            pdf_customer_data,
            colWidths=[170, 100, 180],
            repeatRows=1
        )

        customer_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BURGUNDY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("BACKGROUND", (0, 1), (-1, -1), BABY_PINK),
            ("TEXTCOLOR", (0, 1), (-1, -1), DARK_BURGUNDY),
            ("GRID", (0, 0), (-1, -1), 0.5, SOFT_PINK),
            ("PADDING", (0, 0), (-1, -1), 7)
        ]))

        content.append(customer_table)

        # Generate PDF
        pdf.build(content)

        pdf_data = buffer.getvalue()

        buffer.close()

        st.success("PDF Report Generated Successfully!")

        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_data,
            file_name="shopping_trend_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )