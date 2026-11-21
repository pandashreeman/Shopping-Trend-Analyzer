import streamlit as st
import pandas as pd

from database.db import get_analysis_history


def show_analysis_history():

    # Page heading
    st.markdown(
        """
        <h1 style="color:#800F3F;">📚 Analysis History</h1>
        <p style="color:#4A1028; font-size:16px;">
            View and download your previously saved analysis records.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Get logged-in user ID
    user_id = st.session_state.user["id"]

    # Fetch analysis history
    history = get_analysis_history(user_id)

    # Check whether history exists
    if history.empty:

        st.info(
            "📭 No analysis history available yet. "
            "Your saved analysis records will appear here."
        )

        return

    # Analysis overview
    st.subheader("📊 History Overview")

    total_records = len(history)
    total_types = history["analysis_type"].nunique()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Analysis Records",
            total_records
        )

    with col2:
        st.metric(
            "Analysis Types",
            total_types
        )

    st.markdown("---")

    # Analysis type summary
    st.subheader("📌 Analysis Type Summary")

    type_summary = (
        history["analysis_type"]
        .value_counts()
        .reset_index()
    )

    type_summary.columns = [
        "Analysis Type",
        "Total Records"
    ]

    st.dataframe(
        type_summary,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Previous analysis records
    st.subheader("🗂️ Previous Analysis Records")

    st.write(
        "Select any record below to view its complete details."
    )

    for index, row in history.iterrows():

        analysis_type = row["analysis_type"]
        created_at = row["created_at"]

        with st.expander(
            f"📄 {analysis_type}  |  {created_at}"
        ):

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#FCE7EF;
                        padding:15px;
                        border-radius:10px;
                        border-left:5px solid #800F3F;
                    ">
                        <p style="color:#800F3F; margin:0;">
                            Analysis ID
                        </p>
                        <h3 style="color:#4A1028; margin:5px 0;">
                            {row['id']}
                        </h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#FCE7EF;
                        padding:15px;
                        border-radius:10px;
                        border-left:5px solid #800F3F;
                    ">
                        <p style="color:#800F3F; margin:0;">
                            Analysis Type
                        </p>
                        <h3 style="color:#4A1028; margin:5px 0;">
                            {analysis_type}
                        </h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("### 📅 Analysis Date")
            st.write(created_at)

            st.markdown("### 📝 Analysis Result")

            st.code(
                str(row["result_data"]),
                language="text"
            )

    # Download section
    st.markdown("---")

    st.subheader("📥 Download Analysis History")

    st.write(
        "Export all your saved analysis records into a CSV file."
    )

    csv_data = history.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download History CSV",
        data=csv_data,
        file_name="analysis_history.csv",
        mime="text/csv",
        use_container_width=True
    )