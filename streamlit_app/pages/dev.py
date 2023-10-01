import streamlit as st

# Не уверен на счёт импорта, работает, но ide ругается
from static.components import render_basement

st.set_page_config(page_title="Developers",
                   page_icon="🤡",
                   layout='wide',
                   initial_sidebar_state='expanded',
                   )

st.write("""
##### NAME SURNAME  
**ROLE**  
B.S. Software Engineering and Computer Science, Ural Federal University  
tg/mail/whatever: [%mycoolname%](https://www.coolsmth.com/in/%mycoolname%/)""")
st.write("")

st.write("""
##### NAME SURNAME  
**ROLE**  
B.S. Software Engineering and Computer Science, Ural Federal University  
tg/mail/whatever: [%mycoolname%](https://www.coolsmth.com/in/%mycoolname%/)""")
st.write("")

st.write("""
##### NAME SURNAME  
**ROLE**  
B.S. Software Engineering and Computer Science, Ural Federal University  
tg/mail/whatever: [%mycoolname%](https://www.coolsmth.com/in/%mycoolname%/)""")
st.write("")

st.write("""
##### NAME SURNAME  
**ROLE**  
B.S. Software Engineering and Computer Science, Ural Federal University  
tg/mail/whatever: [%mycoolname%](https://www.coolsmth.com/in/%mycoolname%/)""")
st.write("")

render_basement()
