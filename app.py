import streamlit as st
from evaluation import evaluate
st.title("Score Project")
csvfile=st.file_uploader("Upload your CSV file", type=["csv"])

if csvfile is not None:
    st.write("Your CSV file has been uploaded.")
    st.write(csvfile)
    score=evaluate(csvfile)
    st.write(score)
else:
    st.write("Please upload your CSV file.")    