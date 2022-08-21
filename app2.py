import streamlit as st
import psycopg2

@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT count(*) from asset_master;")
for row in rows:    
    ct = row[0]
ic_request = run_query("select count(*) from incoming_request;")
for rc in ic_request:    
    ct1=rc[0]

st.title("Dashboard")
c=st.empty()
with c.container():
    kpi1,kpi2 = st.columns(2)
    kpi1.metric(label="Assets", value=ct)
    kpi2.metric(label="Incoming Request", value=ct1)


# Print results.
#for row in rows:
 #   st.write(f"{row[0]} has a :{row[1]}:")