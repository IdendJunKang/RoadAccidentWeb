import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://swartzlaw.com/wp-content/uploads/2023/05/car.jpg");
background-repeat: no-repeat;
background-size:cover;
}
[data=testid="stHeader"]{
background-color=rgba(0,0,0,0);
}
</style>
"""

st.markdown(page_bg_img,unsafe_allow_html=True)


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

page = st.sidebar.selectbox("Explore/Predict", ("Explore", "Predict"))

if page == 'Predict':
    show_predict_page()
else:
    show_explore_page()