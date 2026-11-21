
import streamlit as st

from database.db import (
    create_table,
    register_user,
    login_user
)

from pages.dashboard import show_dashboard


# Set page configuration
st.set_page_config(
    page_title="Shopping Trend Analyzer",
    page_icon="🛍️",
    layout="wide"
)


# Load CSS styling
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# Create database tables
create_table()


# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None


# Hide sidebar on login and registration pages
if not st.session_state.logged_in:

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="collapsedControl"] {
            display: none !important;
        }

        [data-testid="stHeader"] {
            background-color: #FCE7EF !important;
        }

        [data-testid="stToolbar"] {
            background-color: #FCE7EF !important;
        }

        [data-testid="stDecoration"] {
            background-color: #800F3F !important;
        }

        .stApp {
            background-color: #FCE7EF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Display login and registration pages
if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="main-title">
            🛍️ SHOPPING TREND ANALYZER
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.3, 1])

    with center:

        # Login page
        if st.session_state.page == "login":

            st.markdown(
                '<div class="auth-title">Welcome Back!</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="auth-subtitle">'
                'Login to continue to your dashboard'
                '</div>',
                unsafe_allow_html=True
            )

            with st.form("login_form"):

                st.subheader("Login")

                email = st.text_input(
                    "Email Address",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_button = st.form_submit_button(
                    "LOGIN",
                    use_container_width=True
                )

                # Check login details
                if login_button:

                    if not email or not password:

                        st.warning(
                            "Please enter email and password."
                        )

                    else:

                        user = login_user(
                            email.lower().strip(),
                            password
                        )

                        if user:

                            st.session_state.logged_in = True
                            st.session_state.user = user

                            st.rerun()

                        else:

                            st.error(
                                "Invalid email or password."
                            )

            # Open registration page
            if st.button(
                "CREATE NEW ACCOUNT",
                use_container_width=True
            ):

                st.session_state.page = "register"
                st.rerun()

        # Registration page
        elif st.session_state.page == "register":

            st.markdown(
                '<div class="auth-title">Create Account</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="auth-subtitle">'
                'Register to get started'
                '</div>',
                unsafe_allow_html=True
            )

            with st.form("register_form"):

                st.subheader("Registration")

                username = st.text_input(
                    "Full Name",
                    placeholder="Enter your name"
                )

                email = st.text_input(
                    "Email Address",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm your password"
                )

                register_button = st.form_submit_button(
                    "REGISTER",
                    use_container_width=True
                )

                # Check registration details
                if register_button:

                    if not username or not email or not password:

                        st.warning(
                            "Please fill in all fields."
                        )

                    elif password != confirm_password:

                        st.error(
                            "Passwords do not match."
                        )

                    elif len(password) < 8:

                        st.error(
                            "Password must contain at least 8 characters."
                        )

                    else:

                        success = register_user(
                            username.strip(),
                            email.lower().strip(),
                            password
                        )

                        if success:

                            st.success(
                                "Registration successful!"
                            )

                            st.session_state.page = "login"

                            st.rerun()

                        else:

                            st.error(
                                "This email is already registered."
                            )

            # Return to login page
            if st.button(
                "BACK TO LOGIN",
                use_container_width=True
            ):

                st.session_state.page = "login"
                st.rerun()


# Display dashboard and other modules
else:

    from pages.dataset import show_dataset

    # Display sidebar heading
    st.sidebar.markdown(
        """
        <div style="text-align:center; padding:10px 0;">
            <h2 style="color:#800F3F; margin-bottom:5px;">
                🛍️ Shopping Analyzer
            </h2>
            <p style="color:#4A1028; font-size:13px;">
                Trend Analysis Dashboard
            </p>
        </div>
        <hr style="border:1px solid #800F3F;">
        """,
        unsafe_allow_html=True
    )

    # Display logged in user
    st.sidebar.markdown(
        f"""
        <div style="
            background-color:#FCE7EF;
            padding:12px;
            border-radius:10px;
            margin-bottom:15px;
        ">
            <p style="color:#800F3F; margin:0;">
                👤 Logged in as
            </p>
            <h4 style="color:#4A1028; margin:5px 0;">
                {st.session_state.user['username']}
            </h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create sidebar navigation
    pages = {
        "🏠 Dashboard": "Dashboard",
        "📂 Dataset Management": "Dataset Management",
        "➕ Add Transaction": "Add Transaction",
        "🧾 View Transactions": "View Transactions",
        "👥 Customer Analysis": "Customer Analysis",
        "📦 Product Analysis": "Product Analysis",
        "💰 Sales Analysis": "Sales Analysis",
        "💡 Smart Insights": "Smart Insights",
        "🤖 Machine Learning": "Machine Learning Analysis",
        "📚 Analysis History": "Analysis History",
        "📊 Reports": "Reports"
    }

    selected_option = st.sidebar.radio(
        "MAIN MENU",
        list(pages.keys())
    )

    selected_page = pages[selected_option]

    # Open selected page
    if selected_page == "Dashboard":

        show_dashboard()

    elif selected_page == "Dataset Management":

        show_dataset()

    elif selected_page == "Add Transaction":

        from pages.data_entry import show_data_entry
        show_data_entry()

    elif selected_page == "View Transactions":

        from pages.transactions import show_transactions
        show_transactions()

    elif selected_page == "Customer Analysis":

        from pages.customer_analysis import show_customer_analysis
        show_customer_analysis()

    elif selected_page == "Product Analysis":

        from pages.product_analysis import show_product_analysis
        show_product_analysis()

    elif selected_page == "Sales Analysis":

        from pages.sales_analysis import show_sales_analysis
        show_sales_analysis()

    elif selected_page == "Smart Insights":

        from pages.smart_insights import show_smart_insights
        show_smart_insights()

    elif selected_page == "Machine Learning Analysis":

        from pages.ml_analysis import show_ml_analysis
        show_ml_analysis()

    elif selected_page == "Analysis History":

        from pages.analysis_history import show_analysis_history
        show_analysis_history()

    elif selected_page == "Reports":

        from pages.reports import show_reports
        show_reports()

    # Logout from application
    st.sidebar.markdown("---")

    if st.sidebar.button(
        "🚪 Logout",
         key="logout_button",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"

        st.rerun()
