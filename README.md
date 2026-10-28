# JobApply AI — Staging Preview

This is a standalone, mock-data-only Streamlit UI preview. It is **not** the production bot and is **not** a secure multi-user service. It has no real scanner, AI tailoring, invitations, durable data, or application submission. Demo approvals only update session state. No resumes are persisted.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy isolated Streamlit staging

1. Create a **separate private GitHub repository** named `jobapply-ai-staging`.
2. Upload only `app.py`, `requirements.txt`, and this `README.md` to the staging repository.
3. In Streamlit Community Cloud, create a **new** app from the staging repository (`main`, `app.py`).
4. Keep the original production app/repository unchanged.
5. Use fake data only. Do not upload personal resumes to this demo; the upload widget is only a UI placeholder.

## Before real multi-user beta

Implement and test authentication, invite-only access, row-level security, encrypted/private resume storage, job ingestion, AI tailoring with confirmation of skills, an approval queue, and verified application submission. Never label approvals as submitted unless the destination confirms receipt.
