import streamlit as st
import pandas as pd
import os
from utils.data_processing import validate_dataset
from utils.data_processing import preprocess_dataset


def show_dataset():

    st.title("📁 Dataset Management")

    st.write("View your shopping dataset or upload a custom CSV file.")

    # Dataset selection
    st.subheader("Select Dataset")

    option = st.radio(
        "Choose Dataset Source:",
        ["Built-in Dataset", "Upload Custom CSV"],
        horizontal=True
    )

    df = None

    # Built-in dataset
    if option == "Built-in Dataset":

        file_path = "datasets/shopping_data.csv"

        if os.path.exists(file_path):

            df = pd.read_csv(file_path)

            st.success("Built-in dataset loaded successfully!")

        else:
            st.error("Built-in dataset not found.")

    # Custom CSV upload
    else:

        uploaded_file = st.file_uploader(
            "Upload your CSV file",
            type=["csv"]
        )

        if uploaded_file is not None:

            try:
                df = pd.read_csv(uploaded_file)

                st.success("CSV file uploaded successfully!")

            except Exception as e:
                st.error(f"Error reading CSV file: {e}")

    # Dataset information
    if df is not None:

        # Dataset Validation
        st.markdown("---")
        st.subheader("Dataset Validation")

        errors, warnings = validate_dataset(df)

        if errors:
            for error in errors:
                st.error(error)

        elif warnings:
            st.warning("Dataset loaded, but some issues were found.")

            for warning in warnings:
                st.warning(warning)

        else:
            st.success("Dataset validation successful! No issues found.")

        st.markdown("---")

        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Records", len(df))

        with col2:
            st.metric("Total Columns", len(df.columns))

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        st.markdown("---")

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("Column Information")

        column_info = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values
        })

        st.dataframe(
            column_info,
            use_container_width=True
        )

        # Data Preprocessing
        st.markdown("---")

        st.subheader("🧹 Data Preprocessing")

        st.write(
            "Clean your dataset by handling missing values, "
            "duplicates and incorrect data."
        )

        if st.button("Preprocess Dataset"):

            original_records = len(df)

            cleaned_df = preprocess_dataset(df)

            cleaned_records = len(cleaned_df)

            st.session_state.cleaned_dataset = cleaned_df

            st.success("Dataset preprocessing completed!")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Original Records",
                    original_records
                )

            with col2:
                st.metric(
                    "Cleaned Records",
                    cleaned_records
                )

            with col3:
                st.metric(
                    "Removed Records",
                    original_records - cleaned_records
                )

        # Display cleaned dataset
        if "cleaned_dataset" in st.session_state:

            st.subheader("Cleaned Dataset Preview")

            st.dataframe(
                st.session_state.cleaned_dataset.head(10),
                use_container_width=True
            )
