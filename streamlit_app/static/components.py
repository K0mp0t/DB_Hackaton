import streamlit as st


def render_basement() -> None:
    """
       Renders the basement section of the webpage.
       This function is responsible for rendering the basement section of the webpage. It includes three columns:
       - Column 1: Displays a text block with contact information and a link to contact us.
       - Column 2: Displays a text block with a link to our LinkedIn page.
       - Column 3: Displays a text block with the copyright information.
       Parameters:
           None
       Returns:
           None
       """
    st.write('---')
    c1, c2, c3 = st.columns((1, 1, 1))

    with c1:
        st.write(
            """Есть вопросы?  
            Свяжитесь с нами: 
            [link](link)""")
    with c2:
        st.write('LinkedIn: [link](link)')
    with c3:
        st.write('© 2023 Команда: AI Talent Hub')

    st.write('---')
