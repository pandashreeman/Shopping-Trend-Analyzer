import streamlit as st
from database.db import add_transaction
from datetime import date
import uuid


def show_data_entry():

    st.title("➕ Add Shopping Transaction")

    st.write("Enter the details of a new shopping transaction.")

    st.markdown("---")

    with st.form("transaction_form"):

        st.subheader("Customer Information")

        col1, col2 = st.columns(2)

        with col1:
            customer_id = st.text_input("Customer ID")

            customer_name = st.text_input("Customer Name")

            age = st.number_input(
                "Customer Age",
                min_value=1,
                max_value=100,
                value=20
            )

        with col2:
            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"]
            )

            purchase_date = st.date_input(
                "Purchase Date",
                value=date.today()
            )

        st.markdown("---")

        st.subheader("Product Information")

        col3, col4 = st.columns(2)

        with col3:

            category = st.selectbox(
                "Product Category",
                [
                    "Electronics",
                    "Clothing",
                    "Grocery",
                    "Beauty",
                    "Furniture"
                ]
            )

            product = st.text_input("Product Name")

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=1000,
                value=1
            )

        with col4:

            purchase_amount = st.number_input(
                "Total Purchase Amount (₹)",
                min_value=0.01,
                value=100.0,
                step=10.0
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "UPI",
                    "Cash",
                    "Credit Card",
                    "Debit Card",
                    "Net Banking"
                ]
            )

        st.markdown("---")

        submitted = st.form_submit_button(
            "Save Transaction",
            use_container_width=True
        )

        if submitted:

            if not customer_id.strip():
                st.error("Please enter Customer ID.")

            elif not customer_name.strip():
                st.error("Please enter Customer Name.")

            elif not product.strip():
                st.error("Please enter Product Name.")

            else:

                transaction_id = "TXN-" + uuid.uuid4().hex[:10].upper()

                transaction_data = (
                    transaction_id,
                    customer_id.strip(),
                    customer_name.strip(),
                    age,
                    gender,
                    product.strip(),
                    category,
                    quantity,
                    purchase_amount,
                    payment_method,
                    purchase_date.strftime("%Y-%m-%d")
                )

                result = add_transaction(transaction_data)

                if result:

                    st.success(
                        "Shopping transaction saved successfully!"
                    )

                    st.info(
                        f"Transaction ID: {transaction_id}"
                    )

                else:

                    st.error(
                        "Unable to save transaction. Please try again."
                    )