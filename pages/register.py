import streamlit as st

from database.db import register_user


def show_register():

    # Hide sidebar on registration page
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

    # Center registration form
    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
            <h1 class="auth-title">🛍️ Create Account</h1>
            <p class="auth-subtitle">
                Join Shopping Trend Analyzer today!
            </p>
            """,
            unsafe_allow_html=True
        )

        with st.form("register_form"):

            st.subheader("Registration")

            username = st.text_input(
                "Username",
                placeholder="Enter your username"
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
                placeholder="Re-enter your password"
            )

            register_button = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if register_button:

                if not username or not email or not password or not confirm_password:

                    st.warning("Please fill in all fields.")

                elif password != confirm_password:

                    st.error("Passwords do not match.")

                elif len(password) < 6:

                    st.warning("Password must contain at least 6 characters.")

                else:

                    success = register_user(
                        username.strip(),
                        email.lower().strip(),
                        password
                    )

                    if success:

                        st.success("Account created successfully!")

                        st.session_state.page = "login"

                        st.rerun()

                    else:

                        st.error(
                            "This email is already registered. "
                            "Please use another email."
                        )

        st.markdown(
            "<p style='text-align:center;'>"
            "Already have an account?"
            "</p>",
            unsafe_allow_html=True
        )

        if st.button(
            "Back to Login",
            use_container_width=True
        ):

            st.session_state.page = "login"
            st.rerun()