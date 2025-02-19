import streamlit as st
from lib.ui import QAFormUI

def main():
    st.set_page_config(page_title="QA Test Report", layout="wide")
    app = QAFormUI()
    app.render()

if __name__ == "__main__":
    main() 