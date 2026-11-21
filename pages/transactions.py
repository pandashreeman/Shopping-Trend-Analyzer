import streamlit as st
from database.db import (
    get_transactions,
    search_transaction,
    update_transaction,
    delete_transaction
)
import pandas as pd

def show_transactions():

    st.title("📋 Shopping Transactions")

    st.write("View and search your shopping transactions.")

    st.markdown("---")

    # Get all transactions
    df = get_transactions()

    # Transaction statistics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Transactions", len(df))

    with col2:
        total_revenue = df["purchase_amount"].sum() if not df.empty else 0

        st.metric(
            "Total Revenue",
            f"₹{total_revenue:,.2f}"
        )

    st.markdown("---")

    # Search transaction
    st.subheader("🔍 Search Transaction")

    transaction_id = st.text_input(
        "Enter Transaction ID"
    )

    if st.button("Search"):

        if transaction_id.strip():

            result = search_transaction(
                transaction_id.strip()
            )

            if result:

                st.success("Transaction found!")

                st.write({
                    "Transaction ID": result[1],
                    "Customer ID": result[2],
                    "Customer Name": result[3],
                    "Age": result[4],
                    "Gender": result[5],
                    "Product": result[6],
                    "Category": result[7],
                    "Quantity": result[8],
                    "Purchase Amount": result[9],
                    "Payment Method": result[10],
                    "Purchase Date": result[11]
                })

            else:
                st.warning("No transaction found.")

        else:
            st.warning("Please enter a Transaction ID.")

    st.markdown("---")

    # Display all transactions
    st.subheader("All Transactions")

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No transactions available yet.")

        # Edit and Delete Transactions
    st.markdown("---")

    st.subheader("✏️ Edit or Delete Transaction")

    if not df.empty:

        transaction_ids = df["transaction_id"].tolist()

        selected_id = st.selectbox(
            "Select Transaction ID",
            transaction_ids
        )

        result = search_transaction(selected_id)

        if result:

            st.markdown("### Edit Transaction")

            with st.form("edit_transaction_form"):

                col1, col2 = st.columns(2)

                with col1:

                    customer_id = st.text_input(
                        "Customer ID",
                        value=str(result[2])
                    )

                    customer_name = st.text_input(
                        "Customer Name",
                        value=str(result[3])
                    )

                    age = st.number_input(
                        "Age",
                        min_value=1,
                        max_value=100,
                        value=int(result[4] or 20)
                    )

                    gender = st.selectbox(
                        "Gender",
                        ["Male", "Female", "Other"],
                        index=["Male", "Female", "Other"].index(
                            result[5]
                        ) if result[5] in ["Male", "Female", "Other"] else 0
                    )

                with col2:

                    product = st.text_input(
                        "Product",
                        value=str(result[6])
                    )

                    category = st.text_input(
                        "Category",
                        value=str(result[7])
                    )

                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        value=max(1, int(result[8] or 1))
                    )

                    purchase_amount = st.number_input(
                        "Purchase Amount",
                        min_value=0.01,
                        value=max(0.01, float(result[9] or 0.01))
                    )

                payment_method = st.text_input(
                    "Payment Method",
                    value=str(result[10] or "")
                )

                purchase_date = st.date_input(
                    "Purchase Date",
                    value=pd.to_datetime(result[11]).date()
                )

                update_button = st.form_submit_button(
                    "Update Transaction"
                )

                if update_button:

                    if not customer_id.strip() or not customer_name.strip() or not product.strip():
                        st.error("Please fill in all required fields.")

                    else:

                        updated_data = (
                            customer_id.strip(),
                            customer_name.strip(),
                            age,
                            gender,
                            product.strip(),
                            category.strip(),
                            quantity,
                            purchase_amount,
                            payment_method.strip(),
                            purchase_date.strftime("%Y-%m-%d")
                        )

                        success = update_transaction(
                            selected_id,
                            updated_data
                        )

                        if success:
                            st.success("Transaction updated successfully!")
                            st.rerun()

                        else:
                            st.error("Unable to update transaction.")

            st.markdown("### Delete Transaction")

            if st.button(
                "🗑️ Delete Selected Transaction",
                type="secondary"
            ):

                success = delete_transaction(selected_id)

                if success:
                    st.success("Transaction deleted successfully!")
                    st.rerun()

                else:
                    st.error("Unable to delete transaction.")

    else:

        st.info("No transactions available to edit or delete.")