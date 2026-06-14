"""
CampusFlow — auth.py
Login and Register pages rendered via Streamlit.
Sets st.session_state.user on successful authentication.
"""

import streamlit as st
from db import login_user, register_user


def render_auth_page():
    """
    Renders the full-screen auth gate.
    Returns immediately if user is already in session.
    """
    if st.session_state.get("user"):
        return  # already authenticated

    st.markdown("""
    <style>
    /* Auth page — center the card */
    .auth-card {
        max-width: 420px;
        margin: 0 auto;
        background: #111111;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 36px 32px 28px;
    }
    .auth-brand {
        text-align: center;
        margin-bottom: 28px;
    }
    .auth-brand-name {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.02em;
    }
    .auth-brand-name span { color: #888888; }
    .auth-brand-tag {
        font-size: 0.62rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #444444;
        margin-top: 4px;
    }
    .auth-section-title {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #555555;
        margin-bottom: 16px;
    }
    .auth-note {
        font-size: 0.75rem;
        color: #555555;
        text-align: center;
        margin-top: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Center the form
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="auth-brand">
            <div class="auth-brand-name">Campus<span>Flow</span></div>
            <div class="auth-brand-tag">AI Operating System</div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["Sign In", "Create Account"])

        # ── Login ──────────────────────────────────────────
        with tab_login:
            with st.form("login_form"):
                st.markdown('<div class="auth-section-title">Student Login</div>',
                            unsafe_allow_html=True)
                username = st.text_input("Username", placeholder="e.g. alex")
                password = st.text_input("Password", type="password",
                                         placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In", use_container_width=True)

            if submitted:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    user = login_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.messages = []   # fresh chat per session
                        st.success(f"Welcome back, {user['name'].split()[0]}.")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

            st.markdown("""
            <div class="auth-note">
                Demo accounts: alex / priya / rahul<br>
                Password = &lt;username&gt;123
            </div>
            """, unsafe_allow_html=True)

        # ── Register ────────────────────────────────────────
        with tab_register:
            with st.form("register_form"):
                st.markdown('<div class="auth-section-title">New Student Account</div>',
                            unsafe_allow_html=True)
                r_name     = st.text_input("Full Name", placeholder="e.g. Arjun Verma")
                r_username = st.text_input("Username", placeholder="Choose a unique username")
                r_password = st.text_input("Password", type="password",
                                           placeholder="Minimum 6 characters")
                r_confirm  = st.text_input("Confirm Password", type="password",
                                           placeholder="Re-enter password")
                r_dept     = st.selectbox("Department", ["CSE", "ECE", "MECH"])
                r_sem      = st.number_input("Semester", min_value=1, max_value=8, value=1)
                r_submit   = st.form_submit_button("Create Account", use_container_width=True)

            if r_submit:
                if not all([r_name, r_username, r_password, r_confirm]):
                    st.error("All fields are required.")
                elif len(r_password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif r_password != r_confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register_user(
                        r_username, r_password, r_name, r_dept, int(r_sem)
                    )
                    if ok:
                        st.success(f"{msg} You can now sign in.")
                    else:
                        st.error(msg)

    # Block everything else until authenticated
    st.stop()
