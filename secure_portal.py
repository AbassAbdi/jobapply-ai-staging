                path = f"{user.id}/{uuid4().hex}/{safe_name(file.name)}"
                content_type = "application/pdf" if file.name.lower().endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                try:
                    c.storage.from_(BUCKET).upload(path, data, {"content-type": content_type, "upsert": "false"})
                    c.table("resumes").insert({"user_id": str(user.id), "name": (label.strip() or file.name)[:120], "storage_path": path, "file_name": safe_name(file.name)}).execute()
                    st.success("Resume uploaded privately.")
                    st.rerun()
                except Exception:
                    # Avoid orphaned file on metadata failure when possible.
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
                    # Delete storage before metadata to preserve authorization checks.
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
