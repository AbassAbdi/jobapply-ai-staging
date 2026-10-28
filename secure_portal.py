
"""Private account and resume management for JobApply AI staging.
Requires Supabase secrets and SQL policies from schema.sql.
"""
import os
import re
from datetime import datetime, timezone
from io import BytesIO
from uuid import uuid4

import streamlit as st
from supabase import create_client

MAX_BYTES = 5 * 1024 * 1024
BUCKET = "private-resumes"


def config():
    try:
        url = st.secrets.get("SUPABASE_URL", "")
        anon = st.secrets.get("SUPABASE_ANON_KEY", "")
        admin_email = st.secrets.get("ADMIN_EMAIL", "")
        service = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")
        return str(url), str(anon), str(admin_email).strip().lower(), str(service)
    except Exception:
        return "", "", "", ""


def configured():
    url, anon, _, _ = config()
    return bool(url and anon)


def client():
    url, anon, _, _ = config()
    return create_client(url, anon)


def current_client():
    token = st.session_state.get("access_token")
    refresh = st.session_state.get("refresh_token")
    if not token or not refresh:
        return None, None
    c = client()
    try:
        session = c.auth.set_session(token, refresh)
        if not session or not session.user:
            raise ValueError("No active session")
        st.session_state.access_token = session.session.access_token
        st.session_state.refresh_token = session.session.refresh_token
        return c, session.user
    except Exception:
        st.session_state.pop("access_token", None)
        st.session_state.pop("refresh_token", None)
        return None, None


def login():
    st.markdown("### Private account sign-in")
    st.caption("Invitation required. This is a separate private workspace; the public demo contains no personal resumes.")
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)
    if submitted:
        try:
            response = client().auth.sign_in_with_password({"email": email.strip(), "password": password})
            st.session_state.access_token = response.session.access_token
            st.session_state.refresh_token = response.session.refresh_token
            st.rerun()
        except Exception as exc:
            message = str(exc).lower()
            if "invalid login credentials" in message or "invalid_credentials" in message:
                st.error("Supabase rejected the email/password combination. Check that the account belongs to the same Supabase project configured in Streamlit Secrets.")
            elif "email not confirmed" in message:
                st.error("Supabase says this email is not confirmed.")
            elif "rate limit" in message or "too many requests" in message:
                st.error("Supabase is rate-limiting login attempts. Wait before trying again.")
            elif "user is banned" in message:
                st.error("Supabase has disabled this account.")
            elif "api key" in message or "invalid jwt" in message:
                st.error("Supabase API key or project configuration was rejected. Check Streamlit Secrets.")
            else:
                st.error(f"Authentication failed ({type(exc).__name__}). The app could not complete the Supabase login request.")
    with st.expander("Set password after accepting invitation"):
        st.info("Use the invitation link in your email to establish your account password. Configure the Supabase invitation redirect URL as described in README.md.")


def accept_invite():
    params = st.query_params
    token_hash = params.get("token_hash")
    kind = params.get("type")
    if token_hash and kind in ("invite", "recovery"):
        try:
            c = client()
            response = c.auth.verify_otp({"token_hash": token_hash, "type": kind})
            if response.session:
                st.session_state.access_token = response.session.access_token
                st.session_state.refresh_token = response.session.refresh_token
                st.query_params.clear()
                st.rerun()
        except Exception:
            st.error("This invitation link is invalid or expired. Ask the administrator for a new invitation.")


def safe_name(name):
    return re.sub(r"[^A-Za-z0-9._ -]", "_", name)[:100]


def resumes_page(c, user):
    st.subheader("My Resumes")
    st.caption("Private files are stored in Supabase Storage and accessible only to your account.")
    with st.form("resume_upload"):
        label = st.text_input("Resume name", placeholder="Cloud Engineer Resume")
        file = st.file_uploader("Upload a Word or PDF resume", type=["docx", "pdf"])
        upload = st.form_submit_button("Save private resume")
    if upload:
        if not file:
            st.warning("Choose a resume file first.")
        elif file.size > MAX_BYTES:
            st.error("Maximum resume size is 5 MB.")
        else:
            data = file.getvalue()
            valid = (file.name.lower().endswith(".pdf") and data.startswith(b"%PDF-")) or (file.name.lower().endswith(".docx") and data.startswith(b"PK"))
            if not valid:
                st.error("File content does not match PDF or DOCX format.")
            else:
                path = f"{user.id}/{uuid4().hex}/{safe_name(file.name)}"
                content_type = "application/pdf" if file.name.lower().endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                try:
                    c.storage.from_(BUCKET).upload(path, data, {"content-type": content_type, "upsert": "false"})
                    c.table("resumes").insert({"user_id": str(user.id), "name": (label.strip() or file.name)[:120], "storage_path": path, "file_name": safe_name(file.name)}).execute()
                    st.success("Resume uploaded privately.")
                    st.rerun()
                except Exception:
                    try:
                        c.storage.from_(BUCKET).remove([path])
                    except Exception:
                        pass
                    st.error("Upload failed. Check your database and storage setup.")
    try:
        records = c.table("resumes").select("id,name,file_name,storage_path,is_active,created_at").order("created_at", desc=True).execute().data or []
    except Exception:
        st.error("Could not load resumes. Ensure schema.sql has been applied.")
        return
    if not records:
        st.info("No resumes uploaded yet.")
    for record in records:
        with st.container(border=True):
            a, b, d = st.columns([3, 1, 1])
            a.markdown(f"**{record['name']}**" + (" · Active" if record["is_active"] else ""))
            if b.button("Set active", key=f"active-{record['id']}", disabled=record["is_active"]):
                try:
                    c.rpc("activate_resume", {"target_resume_id": record["id"]}).execute()
                    st.rerun()
                except Exception:
                    st.error("Could not switch resume.")
            if d.button("Delete", key=f"delete-{record['id']}"):
                try:
                    c.storage.from_(BUCKET).remove([record["storage_path"]])
                    c.table("resumes").delete().eq("id", record["id"]).execute()
                    st.rerun()
                except Exception:
                    st.error("Could not delete this resume.")
            if st.button("Download", key=f"get-{record['id']}"):
                try:
                    payload = c.storage.from_(BUCKET).download(record["storage_path"])
                    st.session_state[f"download-{record['id']}"] = payload
                except Exception:
                    st.error("Download failed.")
            if f"download-{record['id']}" in st.session_state:
                st.download_button("Save file", st.session_state[f"download-{record['id']}"], file_name=record["file_name"], key=f"save-{record['id']}")


def invitations_page(user):
    _, _, admin_email, service_key = config()
    if not admin_email or (user.email or "").lower() != admin_email:
        st.error("Administrator access only.")
        return
    st.subheader("Invite a user")
    st.caption("Only the designated administrator can send invitations. Public sign-up must be disabled in Supabase Auth settings.")
    if not service_key:
        st.warning("Administrator invitation service is not configured yet.")
        return
    with st.form("invite"):
        email = st.text_input("Invitee email")
        send = st.form_submit_button("Send invitation")
    if send:
        email = email.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            st.error("Enter a valid email address.")
            return
        try:
            url, _, _, _ = config()
            admin = create_client(url, service_key)
            admin.auth.admin.invite_user_by_email(email)
            st.success("Invitation requested. The invitee should check their email.")
        except Exception:
            st.error("Invitation failed. Check Auth email settings and quotas.")


def secure_portal():
    st.markdown("""<style>[data-testid='stAppViewContainer']{background:#07101e;color:#edf4ff} [data-testid='stHeader']{background:#07101e}</style>""", unsafe_allow_html=True)
    st.title("🤖 JobApply AI")
    st.caption("Secure staging · Invite-only accounts · Private resumes")
    accept_invite()
    c, user = current_client()
    if not user:
        login()
        return
    st.sidebar.success(f"Signed in: {user.email}")
    page = st.sidebar.radio("Workspace", ["My Resumes", "My Search Profiles", "Approval Queue", "Application History", "Manage Invitations", "Account"])
    if st.sidebar.button("Sign out"):
        try:
            c.auth.sign_out()
        except Exception:
            pass
        st.session_state.clear()
        st.rerun()
    if page == "My Resumes":
        resumes_page(c, user)
    elif page == "Manage Invitations":
        invitations_page(user)
    elif page == "Account":
        st.subheader("Account")
        st.write(f"Signed in as {user.email}")
        with st.form("password"):
            password = st.text_input("New password (at least 12 characters)", type="password")
            change = st.form_submit_button("Update password")
        if change:
            if len(password) < 12:
                st.error("Use at least 12 characters.")
            else:
                try:
                    c.auth.update_user({"password": password})
                    st.success("Password updated.")
                except Exception:
                    st.error("Password update failed.")
    else:
        st.subheader(page)
        st.info("Private workspace created. This feature will be connected in the next phase; no applications are submitted.")
