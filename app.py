import streamlit as st
from evaluation import evaluate
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(page_title="Score Project", page_icon=":trophy:")

# --- Page Navigation ---
pages = {
    "Home": "Get your project score",
    "Challenge": "Download, clean, and re-upload",
    "Leaderboard": "See who's on top!",
}
page = st.sidebar.radio("Select a page:", tuple(pages.keys()))

# --- Helper Functions ---


def save_leaderboard(name, score):
    if not os.path.exists("leaderboard.csv"):
        leaderboard = pd.DataFrame(columns=["Name", "Score"])
    else:
        leaderboard = pd.read_csv("leaderboard.csv")

    new_row = pd.DataFrame({"Name": [name], "Score": [score]})  # Create a DataFrame for the new row
    leaderboard = pd.concat([leaderboard, new_row], ignore_index=True)  # Use concat to append the new row
    leaderboard = leaderboard.sort_values(by="Score", ascending=False).reset_index(drop=True)
    leaderboard.to_csv("leaderboard.csv", index=False)
    leaderboard.to_csv("leaderboard.csv", index=False) 

# --- Home Page ---
if page == "Home":
    st.title("Score Project - Home")
    csvfile = st.file_uploader("Upload your CSV file", type=["csv"])

    if csvfile is not None:
        st.write("Your CSV file has been uploaded.")
        score,list_of_hints = evaluate(csvfile)
        st.markdown("---")  # Separator for better visual separation
        st.header("Your Score")
        # Display the progress bar and inject the JavaScript
        st.write(f"Your score is: {score:.2f}")
        # Option 3: Using a colored box
        if score >= 80:
            st.success(f"Your score is: **{score}**. Excellent!")
        elif score >= 60:
            st.info(f"Your score is: **{score}**. Good!")
        else:
            st.warning(f"Your score is: **{score}**. Needs improvement.")
        if list_of_hints:
            st.markdown("---")
            st.write("Things to improve:")
            for hint in list_of_hints:
                st.caption("* "+hint)


    else:
        st.write("Please upload your CSV file.")
        
# --- Challenge Page ---
elif page == "Challenge":
    st.title("Score Project - Challenge")
    st.markdown("""
                ## The Challenge:

                **Your mission, if you choose to accept it, is to improve the quality of the provided dataset and achieve a higher score!**
     
                1. **Download the sample CSV file:** This file contains a dataset with some data quality issues.
                2. **Clean and preprocess the data:** Use your data cleaning and preprocessing skills to address the issues in the dataset. 
                This might involve:
                    - Handling missing values
                    - Correcting data types
                    - Removing duplicates
                    - And any other techniques you deem necessary.
                3. **Re-upload the cleaned CSV file:** Once you're satisfied with your cleaning efforts, upload the improved dataset.
                4. **Get your new score:** Your cleaned dataset will be evaluated, and you'll receive a new score. 
                **Try to beat your previous score or climb the leaderboard!**
                """)
    # Download sample CSV
    sample_csv = pd.read_csv("./Tuwaiq Students.csv")
    st.download_button(
        label="Download Tuwaiq Students CSV file",
        data=sample_csv.to_csv(index=False),
        file_name="Tuwaiq Students1.csv",
        mime="text/csv",
    )

    # Upload cleaned CSV
    cleaned_csv = st.file_uploader("Upload your cleaned CSV file", type=["csv"])
    if cleaned_csv is not None:
        st.write("Your cleaned CSV file has been uploaded.")
        cleaned_score,list_of_hints = evaluate(cleaned_csv)
        
        if cleaned_score >= 80:
            st.success(icon="✅",body= f"Your cleaned score is: **{cleaned_score}**. Excellent!")
        elif cleaned_score >= 60:
            st.info(body= f"Your cleaned score is: **{cleaned_score}**. Good!")
        else:
            st.warning(icon="⚠️",body= f"Your cleaned score is: **{cleaned_score}**. Needs improvement.")
        name = st.text_input("Enter your name for the leaderboard:")
        if name and st.button("Submit Score"):
            save_leaderboard(name, cleaned_score)
            st.success("Score submitted!")
    else:
        st.write("Please upload your cleaned CSV file.")
elif page == "Leaderboard":
    st.title("Leaderboard")
    if os.path.exists("leaderboard.csv"):
        leaderboard = pd.read_csv("leaderboard.csv")
        st.table(leaderboard)
    else:
        st.write("Leaderboard is empty.")