import streamlit as st
from requests import post

def main() -> None:
    frontend = Frontend()

class Frontend():

    def __init__(self):
        
        st.title("DataViewer")

        file = st.file_uploader("Envie o CSV", type="csv")

        if file:
            pass


