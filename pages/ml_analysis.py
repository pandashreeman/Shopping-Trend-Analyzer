import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from database.db import get_transactions, save_analysis
from utils.visualization import create_line_chart


def show_ml_analysis():

    st.title("🤖 Machine Learning Analysis")

    st.write(
        "Use machine learning to analyze shopping data "
        "and predict future sales."
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

    # Prepare sales data
    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"],
        errors="coerce"
    )

    df = df.dropna(subset=["purchase_date"])

    if df.empty:
        st.warning("No valid purchase dates available.")
        return

    # Group sales by date
    daily_sales = df.groupby(
        df["purchase_date"].dt.date
    )["purchase_amount"].sum().reset_index()

    daily_sales.columns = [
        "Date",
        "Total_Sales"
    ]

    daily_sales = daily_sales.sort_values(
        by="Date"
    ).reset_index(drop=True)

    # Display sales data
    st.subheader("📊 Daily Sales Data")

    st.dataframe(
        daily_sales,
        use_container_width=True,
        hide_index=True
    )

    # Check minimum records
    if len(daily_sales) < 2:
        st.warning(
            "At least two different sales dates are required "
            "to train the machine learning model."
        )
        return

    st.markdown("---")

    # Train Linear Regression Model
    st.subheader("🧠 Sales Prediction Model")

    # Create numerical day values
    daily_sales["Day_Number"] = range(len(daily_sales))

    # Prepare input and output
    X = daily_sales[["Day_Number"]]
    y = daily_sales["Total_Sales"]

    # Create Linear Regression Model
    model = LinearRegression()

    # Train the model
    model.fit(X, y)

    # Predict sales
    predictions = model.predict(X)

    # Calculate model performance
    mae = mean_absolute_error(y, predictions)
    r2 = r2_score(y, predictions)

    # Display model performance
    st.success("Machine Learning Model Trained Successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Mean Absolute Error",
            f"₹{mae:,.2f}"
        )

    with col2:
        st.metric(
            "R² Score",
            f"{r2:.2f}"
        )

    st.markdown("---")

    # Actual vs Predicted Sales
    st.subheader("📈 Actual vs Predicted Sales")

    fig1, ax1 = plt.subplots(figsize=(10, 5))

    create_line_chart(
        ax1,
        daily_sales["Day_Number"],
        y,
        "Actual vs Predicted Daily Sales",
        "Day Number",
        "Sales Amount (₹)"
    )

    # Add predicted sales line
    ax1.plot(
        daily_sales["Day_Number"],
        predictions,
        color="#F4B6CC",
        marker="x",
        linestyle="--",
        linewidth=2,
        label="Predicted Sales"
    )

    ax1.plot(
        daily_sales["Day_Number"],
        y,
        color="#800F3F",
        marker="o",
        linewidth=2,
        label="Actual Sales"
    )

    ax1.legend()

    plt.tight_layout()

    st.pyplot(fig1)
    plt.close(fig1)

    # Prediction Details
    prediction_results = daily_sales.copy()

    prediction_results["Predicted_Sales"] = predictions

    st.subheader("Prediction Results")

    st.dataframe(
        prediction_results[
            ["Date", "Total_Sales", "Predicted_Sales"]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Future Sales Forecast
    st.subheader("🔮 Future Sales Forecast")

    forecast_days = st.number_input(
        "Select Number of Future Days",
        min_value=1,
        max_value=30,
        value=7,
        step=1
    )

    if st.button("Generate Sales Forecast"):

        # Create future day numbers
        future_days = range(
            len(daily_sales),
            len(daily_sales) + int(forecast_days)
        )

        future_data = pd.DataFrame({
            "Day_Number": list(future_days)
        })

        # Predict future sales
        future_predictions = model.predict(
            future_data[["Day_Number"]]
        )

        # Avoid negative sales predictions
        future_predictions = future_predictions.clip(min=0)

        # Generate future dates
        last_date = pd.to_datetime(
            daily_sales["Date"].iloc[-1]
        )

        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=int(forecast_days)
        )

        # Create forecast table
        forecast_results = pd.DataFrame({
            "Date": future_dates.date,
            "Predicted_Sales": future_predictions
        })

        # Save forecast in analysis history
        user_id = st.session_state.user["id"]

        result_data = forecast_results.to_json(
            orient="records"
        )

        save_analysis(
            user_id,
            "Future Sales Forecast",
            result_data
        )

        st.success("Future Sales Forecast Generated!")

        # Display forecast
        st.dataframe(
            forecast_results,
            use_container_width=True,
            hide_index=True
        )

        # Display forecast chart
        fig2, ax2 = plt.subplots(figsize=(10, 5))

        create_line_chart(
            ax2,
            forecast_results["Date"],
            forecast_results["Predicted_Sales"],
            "Future Sales Forecast",
            "Future Date",
            "Predicted Sales (₹)"
        )

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig2)
        plt.close(fig2)