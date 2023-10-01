from io import StringIO

import numpy as np
import pandas as pd
import streamlit as st
import requests
from math_and_logic import get_plotly_fig
# Не уверен на счёт импорта, работает, но ide ругается
from static.components import render_basement

# TODO: Change page_title
# hint: run with: streamlit run .\streamlit_app\app.py
# hint: see https://docs.streamlit.io/library/advanced-features/configuration for setting up port
# and enableCORS = false if somthing dosent work
import json

st.set_page_config(layout="wide",
                   page_title="Hackaton Prediction App",
                   page_icon=":airplane:",
                   initial_sidebar_state="expanded")

st.write("<h1><i>STREAMLIT ON AIR. COOL HEADER</i></h1>",
         unsafe_allow_html=True)
st.write('---')

predicted = np.random.randn(20)
real = np.random.randn(20)
cause_of_troubles = None
cause_of_troubles_metrica = None

uploaded_files = st.file_uploader('Upload a CSV file', accept_multiple_files=True, type=['csv'])
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)

    # TODO: requests.post(st.secrets['base_route'] + ..., files=uploaded_file)
    # from request:
    predicted = np.random.randn(20)
    real = np.random.randn(20)
    cause_of_troubles = 'URAl Airlines'
    cause_of_troubles_metrica = 'dead dead dead'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'start': 9500,
    'stop': 10000,
}
if 'response' not in st.session_state:
    print(1)
    st.session_state['response'] = requests.post('http://localhost:5000/predict', headers=headers, json=json_data)
    print(2)
a = json.loads(st.session_state['response'].content)
predicted = json.loads(a['predictions'])
real = json.loads(a['real'])
dataframe = pd.DataFrame().from_dict({'predictions': predicted, 'real': real})
st.line_chart(dataframe, color=["#cf9117", "#94e5ff"])
# Main part
# hint:
# use
# - st.metric
# - Chart elements
#   - st.line_chart
#   - st.bar_chart
#   - st.pyplot
# plotly and altair available

st.write(f'Cause of troubles: {cause_of_troubles}')
cols = st.columns((1, 1, 1, 1))
for i, col in enumerate(cols):
    with col:
        st.metric(f"Metric {i} {cause_of_troubles_metrica}", f'{50 + (i * 4)} шт.', delta=f'{15 - (i * 4)} шт.',
                  delta_color='inverse')

# st.plotly_chart(get_plotly_fig(), theme="streamlit", use_container_width=True)
render_basement()
