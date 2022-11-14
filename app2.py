from cgitb import reset
import streamlit as st
import psycopg2
import pandas as pd
from st_aggrid import AgGrid
from ts import time_series as ts

st.set_page_config(layout='wide', page_title="Dashboard - Flexibility")

@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

@st.experimental_memo(ttl=150)
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

event_rows = run_query("select count(*) from event_table;")
for rc in event_rows:
    ct2=rc[0]


st.title("Flexibility Signals Board")
#c=st.empty()
with st.container():
    kpi1,kpi2,kpi3 = st.columns(3)
    kpi1.metric(label="Total Assets", value=ct)
    kpi2.metric(label="Incoming Request", value=ct1)
    kpi3.metric(label="Events", value=ct2 )
with st.container():
    col1,col2 = st.columns(2)
    with col1:
        st.header("DSO - INCOMING REQUESTS")
        v="WPD"
        query= f"select request_code, dso, zone_id, programme, status, received_time from incoming_request where dso='WPD'"
        result = run_query(query=query)
        cols1=["Request Code","DSO","ZONE", "PROGRAMME","STATUS","RECEIVED TIME"]
        #result = run_query(f"select 'request_code', 'dso', 'zone_id', 'programme', 'status', 'received_time' from incoming_request where 'dso'='"{v}"';")
        df_res=pd.DataFrame(data=result, columns=cols1)
        AgGrid(df_res)
        
    with col2:
        st.header("EVENTS TRIGGERED - CLIENT PARTNERS")
        res = run_query("select req_code, event_type, event_url, status from event_table;")
        cols = ["Request Code", 'Event Type','Event Url','Status']
        df = pd.DataFrame(data=res,columns=cols)
        #df
        AgGrid(df)
        
with st.container():
    col21,col22 = st.columns(2)
    with col21:
        st.header("CLIENT PARTNER - METER READINGS")
        ts_data = ts()
        ds = ts_data.fetch_data()
        AgGrid(ds)
    with col22:
        st.header("DSO - POST METER READINGS")
        result_q = run_query("select transaction_code, request_code, meter_reading, start_time from transaction_details")
        cols3=["Transaction Code", "Request Code", "Meter Reading", "Time" ]
        df1_r= pd.DataFrame(data=result_q,columns=cols3)
        AgGrid(df1_r)
    
    
