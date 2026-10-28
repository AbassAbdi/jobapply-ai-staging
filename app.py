import streamlit as st
from datetime import datetime

st.set_page_config(page_title='JobApply AI | Staging', page_icon='✦', layout='wide', initial_sidebar_state='expanded')
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp{font-family:Inter,system-ui,sans-serif!important}
.stApp{background:#0b1120;color:#e9eefb}
[data-testid="stSidebar"]{background:#101a2e;border-right:1px solid #263451}
[data-testid="stSidebar"] .stMarkdown p{color:#bdc9df}
.block-container{padding-top:1.5rem;max-width:1750px;padding-left:2rem;padding-right:2rem}
h1,h2,h3{color:#f4f7ff!important;letter-spacing:-.03em}
h1{font-size:2rem!important}h3{font-size:1.1rem!important}
.stButton>button[kind="primary"]{background:#635bff;color:white;border:0}
.stButton>button{border-radius:9px;min-height:39px;border:1px solid #344663;background:#192740;color:#f1f5ff}
.stButton>button:hover{border-color:#8078ff;color:#fff}
[data-testid="stMetric"]{background:#151f34;border:1px solid #293753;padding:18px;border-radius:14px;min-height:118px}
[data-testid="stMetricLabel"]{color:#a7b7d3}
[data-testid="stMetricValue"]{color:#f5f7ff}
[data-testid="stVerticalBlockBorderWrapper"]>div{border-color:#2b3b58!important;border-radius:14px!important}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{background:#121d30;color:#f4f7ff;border-color:#34435f}
[data-testid="stSelectbox"]>div>div,[data-testid="stMultiSelect"]>div>div{background:#121d30;color:#e9efff;border-color:#34435f}
hr{border-color:#293753}
.small-muted{color:#95a8c8;font-size:.83rem}
.hero{background:linear-gradient(110deg,#182c55,#242052 65%,#181c39);border:1px solid #3a437c;border-radius:17px;padding:22px 25px;margin:9px 0 21px}
.hero h2{margin:0 0 6px;font-size:1.45rem}.hero p{margin:0;color:#c1cbed;font-size:.88rem}
.jobcard{background:#151f34;border:1px solid #2d3b56;border-radius:12px;padding:15px 16px;margin:0 0 10px}
.jobcard.active{border-color:#786dff;background:#1a2343}
.jobtitle{font-weight:750;color:#f4f7ff;font-size:.99rem;margin-bottom:4px}
.jobmeta{color:#a8b8d1;font-size:.78rem;line-height:1.7}
.pill{display:inline-block;background:#253655;border:1px solid #3b4d6c;border-radius:6px;padding:3px 7px;margin:6px 5px 0 0;color:#c4d4f4;font-size:.72rem}
.pill.green{background:#123e35;border-color:#276f56;color:#8ee6b4}
.pill.purple{background:#322959;border-color:#5b4fa0;color:#c9baff}
.sectionline{font-weight:750;font-size:1.02rem;color:#f1f5ff;margin:8px 0 13px}
.doc{background:#f8faff;color:#273047;padding:22px;border-radius:10px;line-height:1.6;min-height:330px;font-size:.82rem}
.doc h4{font-size:1.05rem;color:#182540;margin:0 0 5px}.doc h5{font-size:.76rem;letter-spacing:.08em;color:#43527b;border-bottom:1px solid #d9dfec;margin:16px 0 7px;padding-bottom:5px}
.doc p,.doc li{color:#34425b}
.notice{border:1px solid #725a32;background:#2d261c;border-radius:9px;padding:10px 13px;color:#f2d5a4;font-size:.82rem}
[data-testid="stRadio"] label p{font-size:.87rem}
</style>''',unsafe_allow_html=True)

JOBS=[
 dict(id='cloud',title='Cloud Support Engineer',company='Northstar Systems (sample)',location='Ottawa, ON · Hybrid',pay='$65–80/hr',score=94,tools=['Azure','Entra ID','Microsoft 365'],desc='Support Microsoft Azure services, Entra ID identity operations, Microsoft 365 and complex cloud incidents. Collaborate with infrastructure teams and document root causes.',category='Cloud'),
 dict(id='admin',title='Senior Systems Administrator',company='Maple Digital (sample)',location='Canada · Remote',pay='$55–70/hr',score=89,tools=['Windows Server','Active Directory','SCCM'],desc='Manage Windows Server, Active Directory, endpoint configuration and service requests. Investigate recurring incidents and improve operational documentation.',category='Systems'),
 dict(id='analyst',title='Application Support Analyst',company='Capital Tech (sample)',location='Gatineau, QC · Hybrid',pay='$52–65/hr',score=86,tools=['ServiceNow','SQL','M365'],desc='Support enterprise applications, triage incidents in ServiceNow, investigate application issues and collaborate with engineering on fixes.',category='Support'),
 dict(id='qa',title='CRM QA Analyst',company='Northern Apps (sample)',location='Canada · Remote',pay='$50–60/hr',score=81,tools=['CRM','Test Cases','ServiceNow'],desc='Test CRM workflows, maintain test cases, record defects and work with application support teams to validate fixes.',category='QA'),
]
DEFAULT_TITLES=['Cloud Engineer','Cloud Support Engineer','System Administrator','Technical Analyst','Application Support Specialist','QA Analyst']
RESUMES=['Cloud Engineer Resume','IT Support Resume','Cybersecurity Resume','QA Analyst Resume']
for k,v in {'selected':'cloud','decisions':{},'resume':RESUMES[0],'mode':'All supported sites','titles':DEFAULT_TITLES[:],'extra_titles':[],'tools':'Azure, Entra ID, Microsoft 365, Active Directory, SCCM, ServiceNow, Exchange Online, SharePoint, Windows Server','saved_urls':'','search_count':0,'resume_names':RESUMES[:],'search_profile':'All IT roles'}.items():
 if k not in st.session_state:st.session_state[k]=v

def job(j):
 active=st.session_state.selected==j['id']
 state=st.session_state.decisions.get(j['id'],'Pending review')
 st.markdown(f'''<div class="jobcard {'active' if active else ''}"><div class="jobtitle">{j['title']}</div><div class="jobmeta">{j['company']}<br>{j['location']} · {j['pay']}</div><span class="pill green">{j['score']}% sample match</span><span class="pill purple">{state}</span></div>''',unsafe_allow_html=True)
 if st.button('View job' if not active else 'Selected',key='select_'+j['id'],use_container_width=True):st.session_state.selected=j['id'];st.rerun()

def preview(j):
 st.markdown(f'''<div class="doc"><h4>Tailored Resume Preview</h4><div style="font-size:.74rem;color:#71809a">ILLUSTRATIVE TEXT — NOT AI-GENERATED</div><h5>PROFESSIONAL SUMMARY</h5><p>Enterprise IT professional supporting complex technology environments, service operations and incident resolution.</p><h5>RELEVANT TECHNOLOGIES</h5><p>{', '.join(j['tools'])}</p><h5>EXPERIENCE HIGHLIGHTS</h5><ul><li>Supported enterprise users and technology services through structured incident investigation.</li><li>Coordinated troubleshooting, escalations and technical documentation.</li></ul><p style="font-size:.72rem;color:#71809a">Real resume tailoring will use the selected user's verified experience and uploaded document.</p></div>''',unsafe_allow_html=True)

with st.sidebar:
 st.markdown('### ✦ JobApply **AI**')
 st.caption('PRIVATE ACCOUNT DESIGN · STAGING')
 st.markdown('---')
 page=st.radio('WORKSPACE',['Dashboard','Find Jobs','Approval Queue','Application History','My Resumes','Job Titles & Profiles','Tools & Experience','Manage Invitations','Settings'],label_visibility='collapsed')
 st.markdown('---')
 st.caption('ACTIVE RESUME')
 st.selectbox('Master resume',st.session_state.resume_names,key='resume',label_visibility='collapsed')
 st.caption('SEARCH MODE')
 st.radio('Search mode',['All supported sites','Specific sites'],key='mode',label_visibility='collapsed')
 if st.session_state.mode=='Specific sites':
  st.multiselect('Search these sites',['LinkedIn','Indeed','Glassdoor','ZipRecruiter','Government of Canada','Employer career sites'],default=['Indeed','Employer career sites'])
  st.text_area('Custom career-page URLs',key='saved_urls',height=78)
 st.caption('SEARCH PREFERENCES')
 st.text_input('Location',value='Ottawa / Gatineau',key='location')
 st.number_input('Minimum CAD/hour',min_value=0,value=50,step=5,key='pay')
 st.checkbox('Remote jobs',value=True,key='remote')
 st.checkbox('Hybrid jobs',value=True,key='hybrid')
 if st.button('↻  Reload search preview',use_container_width=True):
  st.session_state.search_count+=1;st.toast('Demo results refreshed. No external job sites were scanned.')
 st.markdown('---')
 st.caption('🧪 DEMO ONLY · No real applications')

st.markdown('<div class="small-muted">✦ JOBAPPLY AI / STAGING ENVIRONMENT</div>',unsafe_allow_html=True)
st.title('Job Application Command Center' if page=='Dashboard' else page)
st.caption('Interactive design preview · Sample jobs only · No real accounts, AI tailoring, job scanning or submissions')

if page=='Dashboard':
 st.markdown('<div class="hero"><h2>Find the right role. Apply with confidence.</h2><p>Your future AI workflow: discover opportunities, tailor resumes, review matches and approve applications — all from one place.</p></div>',unsafe_allow_html=True)
 a,b,c,d=st.columns(4)
 a.metric('Sample job matches',len(JOBS));b.metric('Awaiting approval',sum(j['id'] not in st.session_state.decisions for j in JOBS));c.metric('Demo approvals',sum(x=='Approved' for x in st.session_state.decisions.values()));d.metric('Real applications','0')
 st.write('')
 left,middle,right=st.columns([1.05,1.25,1.08],gap='medium')
 with left:
  st.markdown('<div class="sectionline">Recommended jobs</div>',unsafe_allow_html=True)
  st.caption(f"{len(JOBS)} sample matches · {st.session_state.mode}")
  for j in JOBS:job(j)
 selected=next(j for j in JOBS if j['id']==st.session_state.selected)
 with middle:
  st.markdown('<div class="sectionline">Job details</div>',unsafe_allow_html=True)
  st.subheader(selected['title']);st.caption(selected['company']+' · '+selected['location'])
  st.markdown(f"**Compensation:** {selected['pay']}  ·  **Sample match:** {selected['score']}%")
  st.markdown('**Job description**');st.write(selected['desc'])
  st.markdown('**Relevant tools**');st.markdown(''.join(f'<span class="pill">{t}</span>' for t in selected['tools']),unsafe_allow_html=True)
  st.write('');st.markdown('**Your decision**')
  x,y=st.columns(2)
  if x.button('✓ Approve (demo)',type='primary',use_container_width=True):st.session_state.decisions[selected['id']]='Approved';st.toast('Demo approval recorded. No application sent.');st.rerun()
  if y.button('✕ Skip',use_container_width=True):st.session_state.decisions[selected['id']]='Skipped';st.toast('Sample job skipped.');st.rerun()
  st.info('Approval is simulated. Web-form submission is not connected.')
 with right:
  st.markdown('<div class="sectionline">Resume preview</div>',unsafe_allow_html=True)
  st.caption('Using: '+st.session_state.resume)
  preview(selected)
  st.button('Download tailored resume · coming soon',disabled=True,use_container_width=True)

elif page in ('Find Jobs','Approval Queue'):
 st.markdown('<div class="hero"><h2>'+('Browse opportunities' if page=='Find Jobs' else 'Review before applying')+'</h2><p>Sample listings illustrate the review experience. Nothing here is a real vacancy.</p></div>',unsafe_allow_html=True)
 query=st.text_input('Search sample job titles, employers or tools',placeholder='e.g. Azure, Cloud, QA')
 subset=[j for j in JOBS if query.lower() in (j['title']+j['company']+' '.join(j['tools'])).lower()]
 if page=='Approval Queue':subset=[j for j in subset if j['id'] not in st.session_state.decisions]
 if not subset:st.info('No matching sample jobs in this view.')
 for j in subset:
  with st.container(border=True):
   st.markdown(f"### {j['title']}");st.caption(j['company']+' · '+j['location']+' · '+j['pay']);st.write(j['desc']);st.caption('Tools: '+', '.join(j['tools']))
   with st.expander('Preview sample tailored resume'):preview(j)
   x,y=st.columns(2)
   if x.button('✓ Approve (demo)',key='approve_'+j['id'],type='primary',use_container_width=True):st.session_state.decisions[j['id']]='Approved';st.rerun()
   if y.button('Skip',key='skip_'+j['id'],use_container_width=True):st.session_state.decisions[j['id']]='Skipped';st.rerun()

elif page=='Application History':
 st.info('This demo records decisions only for the current Streamlit session. No applications are submitted or permanently stored.')
 q=st.text_input('Search demo history',placeholder='Search by title, company or technology')
 records=[j for j in JOBS if j['id'] in st.session_state.decisions and q.lower() in (j['title']+j['company']+' '.join(j['tools'])).lower()]
 if not records:st.write('No demo decisions yet. Visit Dashboard or Approval Queue to try Approve or Skip.')
 for j in records:
  with st.expander(f"{j['title']} · {j['company']} · {st.session_state.decisions[j['id']]}"):
   st.write('**Job description:** '+j['desc']);st.write('**Master resume selected:** '+st.session_state.resume);st.write('**Submission status:** Not submitted (demo)');preview(j)

elif page=='My Resumes':
 st.markdown('<div class="hero"><h2>Master resume library</h2><p>Switch between resume profiles to preview how the experience will work.</p></div>',unsafe_allow_html=True)
 st.selectbox('Active resume',st.session_state.resume_names,key='active_resume_view',index=st.session_state.resume_names.index(st.session_state.resume))
 if st.button('Set as active resume'):st.session_state.resume=st.session_state.active_resume_view;st.rerun()
 st.file_uploader('Upload a sample resume (not stored)',type=['docx','pdf'],help='Files are not persisted in this staging preview. Do not upload real personal resumes.')
 st.warning('No private user storage is connected. Do not upload real resumes to this public demo.')
 for name in st.session_state.resume_names:st.markdown(f'<div class="jobcard"><div class="jobtitle">📄 {name}</div><div class="jobmeta">Example profile · No document stored</div></div>',unsafe_allow_html=True)

elif page=='Job Titles & Profiles':
 st.markdown('<div class="hero"><h2>Personalize your job search</h2><p>Choose target roles and add your own. Settings here are temporary demo state.</p></div>',unsafe_allow_html=True)
 options=list(dict.fromkeys(DEFAULT_TITLES+['Cybersecurity Analyst','ServiceNow Administrator']+st.session_state.extra_titles))
 st.multiselect('Target job titles',options,key='titles')
 new_title=st.text_input('Add a custom job title')
 if st.button('Add job title') and new_title.strip():
  if new_title.strip() not in st.session_state.extra_titles:st.session_state.extra_titles.append(new_title.strip())
  if new_title.strip() not in st.session_state.titles:st.session_state.titles.append(new_title.strip())
  st.rerun()
 st.caption('Switch your active master resume in the left sidebar and click Reload search preview. This does not perform live discovery.')

elif page=='Tools & Experience':
 st.markdown('<div class="hero"><h2>Your verified technology experience</h2><p>In the finished platform, users confirm the tools they know before those skills appear in tailored resumes.</p></div>',unsafe_allow_html=True)
 st.text_area('Tools you have experience with',key='tools',height=180)
 st.caption('Changes here are temporary and are not added to real resumes.')

elif page=='Manage Invitations':
 st.markdown('<div class="hero"><h2>Invite-only access</h2><p>Platform administrators will invite users, who receive their own private resumes, searches and application history.</p></div>',unsafe_allow_html=True)
 st.text_input('Invitee email',placeholder='person@example.com');st.button('Send invitation · not connected',disabled=True)
 st.warning('Real authentication, invitations and user isolation are not implemented in this public staging demo.')

else:
 st.markdown('<div class="hero"><h2>Search and account settings</h2><p>The future production platform will store preferences separately for each invited user.</p></div>',unsafe_allow_html=True)
 st.write('**Selected resume:** '+st.session_state.resume)
 st.write('**Search mode:** '+st.session_state.mode)
 st.write('**Selected titles:** '+', '.join(st.session_state.titles))
 st.write('**Minimum pay:** CAD $'+str(st.session_state.pay)+'/hour')
 st.info('This is a visual staging environment. Preferences are not saved permanently.')

st.divider();st.caption('JobApply AI · Staging design preview · Fictional jobs and sample data · No applications submitted')
