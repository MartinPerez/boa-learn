import plotly.express as px
import streamlit as st
import pandas as pd
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()

datasets = ['National Health and Nutrition Examination Survey','Framingham Heart Study','UK Biobank','Mass General Biobank']
dataset = st.selectbox('Dataset', datasets, disabled=True)

measures = ['None','Gender','Glucose','Biological Age']
measure = st.selectbox('Category', measures)

df=pd.read_csv('2010.csv',index_col=0)
T=df.PERMTH_EXM
E=df.MORTSTAT
if measure=='None':
        kmf.fit(T, E)  
        val=kmf.survival_function_
        val.columns=['Survival']
        val['Time (months)']=val.index  
        fig = px.line(
            val,
            x="Time (months)",
            y="Survival",
            #color="RIAGENDR",
            hover_name="Survival",
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
if measure=='Gender':
        col='RIAGENDR'
        groups = df[col]
        ix = (groups == 1)
        kmf.fit(T[ix], E[ix], label='Male')
        v1 =kmf.survival_function_
        kmf.fit(T[~ix], E[~ix], label='Female')
        v2 =kmf.survival_function_
        v1.columns=['Survival']
        v1['Category']='Male'
        v2.columns=['Survival']
        v2['Category']='Female'
        val=pd.concat([v2,v1])
        val['Time (months)']=val.index
        fig = px.line(
            val,
            x="Time (months)",
            y="Survival",
            color='Category',
            hover_name="Survival",
        )  
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
