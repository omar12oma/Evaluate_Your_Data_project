import streamlit as st
from evaluation import evaluate
import pandas as pd

st.title("Score Project")
csvfile=st.file_uploader("Upload your CSV file", type=["csv"])

if csvfile is not None:
    st.write("Your CSV file has been uploaded.")
    # df = pd.read_csv(csvfile)
    # st.write(df)
    # st.write(csvfile)
    

    score=evaluate(csvfile)*10
    # st.markdown("---")  # Separator for better visual separation
    # st.header("Your Score")
    
    # # Option 1: Using a metric card
    # st.metric(label="", value=str(score))
        # Option 2: Using a progress bar (if score is a percentage)
    # if 0 <= score <= 10:
    #     st.progress(score)
    #     st.write(f"Your score is: {score}%") 
    
    # Option 3: Using a colored box
    if score >= 80:
        st.success(f"Your score is: **{score}**. Excellent!")
    elif score >= 60:
        st.info(f"Your score is: **{score}**. Good!")
    else:
        st.warning(f"Your score is: **{score}**. Needs improvement.")
else:
    st.write("Please upload your CSV file.")
