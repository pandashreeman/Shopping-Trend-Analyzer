import streamlit as st

from database.db import login_user


def show_login():

    # Hide sidebar on login page
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
        </style>
        """,
        unsafe_allow_html=True
    )

    # Center login form
    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
            <h1 class="auth-title">🛍️ Shopping Trend Analyzer</h1>
            <p class="auth-subtitle">
                Welcome back! Please login to continue.
            </p>
            """,
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
                "Login",
                use_container_width=True
            )

            if login_button:

                if not email or not password:

                    st.warning("Please enter your email and password.")

                else:

                    user = login_user(
                        email.lower().strip(),
                        password
                    )

                    if user:

                        st.session_state.logged_in = True
                        st.session_state.user = user

                        st.success("Login successful!")

                        st.rerun()

                    else:

                        st.error("Invalid email or password.")

        st.markdown(
            "<p style='text-align:center;'>"
            "Don't have an account?"
            "</p>",
            unsafe_allow_html=True
        )

        if st.button(
            "Create New Account",
            use_container_width=True
        ):

            st.session_state.page = "register"
            st.rerun()