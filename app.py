import streamlit as st
st.set_page_config(page_title='JobApply AI — STAGING',page_icon='🧪',layout='wide')
st.markdown('''<style>.stApp{background:#081526;color:#edf3ff}div[data-testid="stMetric"]{background:#11243b;padding:18px;border:1px solid #233f60;border-radius:14px}.block-container{padding-top:1.5rem} </style>''',unsafe_allow_html=True)
st.title('🤖 JobApply AI  ·  STAGING DEMO')
st.caption('Visual and workflow preview only • Sample jobs • No real job scanning, AI calls, account creation, or applications')
with st.sidebar:
 st.header('🧪 Demo controls')
 st.warning('DEMO MODE — no real applications can be submitted.')
 page=st.radio('Navigate',['Dashboard','Find Jobs','Approval Queue','Application History','My Resumes','Job Titles & Profiles','Tools & Experience','Manage Invitations'])
 st.divider()
 resume=st.selectbox('Active master resume',['Cloud Engineer Resume','IT Support Resume','Cybersecurity Resume','QA Analyst Resume'])
 mode=st.radio('Search mode',['All supported sites','Specific sites'])
 if mode=='Specific sites':
  st.multiselect('Sites',['LinkedIn','Indeed','Glassdoor','ZipRecruiter','Government of Canada','Employer career websites'],default=['Indeed','Employer career websites'])
  st.text_area('Custom career URLs',placeholder='https://example.com/careers')
 st.text_input('Location','Ottawa / Gatineau')
 st.number_input('Minimum CAD/hour',value=50,min_value=0)
 st.checkbox('Remote',value=True);st.checkbox('Hybrid',value=True)
 st.button('Reload search (demo)',use_container_width=True,help='Refreshes the demo view only')
JOBS=[{'title':'Cloud Engineer','company':'Example Cloud Co.','location':'Ottawa (Hybrid)','pay':'$60–75/hr','tools':'Azure, Entra ID, Microsoft 365','description':'Example listing: Support Azure services, Entra ID, Microsoft 365, and incident response.'},{'title':'IT Systems Administrator','company':'Sample Public Agency','location':'Gatineau (Hybrid)','pay':'$52–60/hr','tools':'Windows Server, Active Directory, SCCM','description':'Example listing: Administer Windows Server, Active Directory, and endpoint tooling.'},{'title':'Cloud Support Specialist','company':'Demo Technology Ltd.','location':'Canada (Remote)','pay':'$55–70/hr','tools':'Azure, Exchange Online, ServiceNow','description':'Example listing: Resolve cloud support incidents and support Exchange Online.'}]
if 'decisions' not in st.session_state:st.session_state.decisions={}
if page=='Dashboard':
 cols=st.columns(4)
 for c,(k,v) in zip(cols,[('Sample matches','3'),('Awaiting approval',str(3-sum(x in ['approved','skipped'] for x in st.session_state.decisions.values()))),('Demo approvals',str(sum(x=='approved' for x in st.session_state.decisions.values()))),('Real submissions','0')]):c.metric(k,v)
 st.subheader('Job matches · sample data')
 for j in JOBS:st.info(f"**{j['title']}** · {j['company']} · {j['location']} · {j['pay']} · {j['tools']}")
 st.caption('Demo metrics do not represent live results.')
elif page in ('Find Jobs','Approval Queue'):
 st.subheader(page)
 for i,j in enumerate(JOBS):
  with st.expander(f"{j['title']} — {j['company']} · {j['pay']}",expanded=i==0):
   st.write(j['description']);st.write('**Relevant tools:** '+j['tools'])
   st.markdown('**Tailored resume preview (sample only)**')
   st.text_area('Preview',f"PROFESSIONAL SUMMARY\nTechnical professional with experience in {j['tools']}.\n\nEXPERIENCE\n• Supported enterprise environments and resolved technical incidents.\n\n[Placeholder only: actual AI tailoring requires a connected service and verified experience.]",height=180,key=f'preview{i}')
   a,b=st.columns(2)
   if a.button('Approve (demo only)',key=f'approve{i}'):
    st.session_state.decisions[i]='approved';st.success('Saved demo approval. Nothing submitted.')
   if b.button('Skip',key=f'skip{i}'):
    st.session_state.decisions[i]='skipped';st.info('Skipped in this demo session.')
elif page=='Application History':
 st.subheader('Application History')
 q=st.text_input('Search job title or employer')
 for i,s in st.session_state.decisions.items():
  j=JOBS[i]
  if q.lower() in (j['title']+' '+j['company']).lower():st.write(f"**{j['title']}** · {j['company']} · Demo decision: {s} · **Not submitted**")
 st.caption('In production, this page will store the exact submitted resume, job description, and verified submission status.')
elif page=='My Resumes':
 st.subheader('My Resumes')
 st.write('Active: **'+resume+'**')
 st.file_uploader('Try the resume upload interface (file is NOT stored)',type=['docx','pdf'])
 st.info('Real private multi-user storage is not connected in this demo.')
elif page=='Job Titles & Profiles':
 st.subheader('Job Titles & Profiles')
 st.multiselect('Target titles',['Cloud Engineer','Cloud Support Engineer','System Administrator','Technical Analyst','QA Analyst','Cybersecurity Analyst','ServiceNow Administrator'],default=['Cloud Engineer','Cloud Support Engineer'])
 st.text_input('Add a custom title')
elif page=='Tools & Experience':
 st.subheader('Tools & Experience')
 st.text_area('Confirmed tools (demo only)','Azure, Entra ID, Microsoft 365, Active Directory, SCCM, ServiceNow')
 st.caption('The production system will require users to confirm tool experience before including it in tailored resumes.')
else:
 st.subheader('Manage Invitations · Admin preview')
 st.text_input('Invitee email')
 st.button('Send invitation (disabled in demo)',disabled=True)
 st.info('Invite-only sign-up and per-user isolation require authentication and database testing before deployment.')
