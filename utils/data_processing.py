import pandas as pd


# Required columns for Shopping Trend Analyzer
REQUIRED_COLUMNS = [
    "Transaction ID",
    "Customer ID",
    "Customer Name",
    "Age",
    "Gender",
    "Product",
    "Category",
    "Quantity",
    "Purchase Amount",
    "Payment Method",
    "Purchase Date"
]


def validate_dataset(df):

    errors = []
    warnings = []

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        errors.append(
            "Missing columns: " + ", ".join(missing_columns)
        )

    # Stop further checks if required columns are missing
    if missing_columns:
        return errors, warnings

    # Check missing values
    missing_values = df[REQUIRED_COLUMNS].isnull().sum()

    for column, count in missing_values.items():
        if count > 0:
            warnings.append(
                f"{column} contains {count} missing values."
            )

    # Check duplicate transactions
    duplicate_count = df["Transaction ID"].duplicated().sum()

    if duplicate_count > 0:
        warnings.append(
            f"Found {duplicate_count} duplicate transaction IDs."
        )

    # Check numeric columns
    numeric_columns = [
        "Age",
        "Quantity",
        "Purchase Amount"
    ]

    for column in numeric_columns:

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        invalid_count = values.isnull().sum()

        if invalid_count > 0:
            warnings.append(
                f"{column} contains {invalid_count} invalid numeric values."
            )

    # Check invalid quantities
    quantity = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    if (quantity <= 0).any():
        warnings.append(
            "Quantity contains zero or negative values."
        )

    # Check invalid purchase amounts
    amount = pd.to_numeric(
        df["Purchase Amount"],
        errors="coerce"
    )

    if (amount < 0).any():
        warnings.append(
            "Purchase Amount contains negative values."
        )

    # Check date format
    dates = pd.to_datetime(
        df["Purchase Date"],
        errors="coerce"
    )

    invalid_dates = dates.isnull().sum()

    if invalid_dates > 0:
        warnings.append(
            f"Found {invalid_dates} invalid purchase dates."
        )

    return errors, warnings

def preprocess_dataset(df):

    # Create a copy so the original dataset remains unchanged
    df = df.copy()

    # Remove duplicate transactions
    df = df.drop_duplicates(
        subset=["Transaction ID"],
        keep="first"
    )

    # Convert numeric columns
    numeric_columns = [
        "Age",
        "Quantity",
        "Purchase Amount"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        df[column] = df[column].fillna(
            df[column].median()
        )

    # Replace invalid quantity values
    df.loc[df["Quantity"] <= 0, "Quantity"] = (
        df["Quantity"].median()
    )

    # Replace negative purchase amounts
    df.loc[df["Purchase Amount"] < 0, "Purchase Amount"] = (
        df["Purchase Amount"].median()
    )

    # Fill missing text values
    text_columns = [
        "Customer Name",
        "Gender",
        "Product",
        "Category",
        "Payment Method"
    ]

    for column in text_columns:
        df[column] = df[column].fillna("Unknown")

    # Convert purchase dates
    df["Purchase Date"] = pd.to_datetime(
        df["Purchase Date"],
        errors="coerce"
    )

    # Remove rows with invalid dates
    df = df.dropna(subset=["Purchase Date"])

    # Convert dates back to readable format
    df["Purchase Date"] = (
        df["Purchase Date"].dt.strftime("%Y-%m-%d")
    )

    return df