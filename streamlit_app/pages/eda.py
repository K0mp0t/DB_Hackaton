import streamlit as st
from static.components import render_basement

st.set_page_config(layout="wide",
                   page_title="Hackaton EDA",
                   page_icon="🤡",
                   initial_sidebar_state="expanded")

st.title("Hackaton EDA")
st.write('Если будет время')

render_basement()
