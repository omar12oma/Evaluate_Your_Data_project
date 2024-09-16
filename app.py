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
def color_gradient(score):
  """Generates a color gradient from red to green based on score (0.0-1.0)."""
  if score < 0.5:
    red = int(255 * (1 - (score * 2)))  # Red decreases linearly from 255 to 0
    green = int(255 * (score * 2))  # Green increases linearly from 0 to 255
  else:
    green = 255
    red = 0  # Red stays at 0
  blue = 0  # No blue component
  return f"rgb({255}, {green}, {blue})"

def save_leaderboard(name, score):
    if not os.path.exists("leaderboard.csv"):
        leaderboard = pd.DataFrame(columns=["Name", "Score"])
    else:
        leaderboard = pd.read_csv("leaderboard.csv")

    new_row = pd.DataFrame({"Name": [name], "Score": [score]})  # Create a DataFrame for the new row
    leaderboard = pd.concat([leaderboard, new_row], ignore_index=True)  # Use concat to append the new row
    leaderboard = leaderboard.sort_values(by="Score", ascending=False).reset_index(drop=True)
    leaderboard.to_csv("leaderboard.csv", index=False) 

# --- Home Page ---
if page == "Home":
    st.title("Score Project - Home")
    csvfile = st.file_uploader("Upload your CSV file", type=["csv"])

    if csvfile is not None:
        st.write("Your CSV file has been uploaded.")
        score = evaluate(csvfile)[0]
        
        score_normalized = score / 10  # Normalize to 0-1 range for color gradient

        st.markdown("---")  # Separator for better visual separation
        st.header("Your Score")

        bar_color = color_gradient(score_normalized)
        

        # Display the progress bar and inject the JavaScript
        st.progress(score_normalized)
        st.write(f"Your score is: {score:.2f}")

        score*=10
        # Option 3: Using a colored box
        if score >= 80:
            st.success(f"Your score is: **{score}**. Excellent!")
        elif score >= 60:
            st.info(f"Your score is: **{score}**. Good!")
        else:
            st.warning(f"Your score is: **{score}**. Needs improvement.")
    else:
        st.write("Please upload your CSV file.")

# --- Challenge Page ---
elif page == "Challenge":
    st.title("Score Project - Challenge")

    # Download sample CSV
    sample_csv = pd.DataFrame({"Column1": [1, 2, 3], "Column2": ["a", "b", "c"]})  # Replace with your actual sample data
    st.download_button(
        label="Download Sample CSV",
        data=sample_csv.to_csv(index=False),
        file_name="sample.csv",
        mime="text/csv",
    )

    # Upload cleaned CSV
    cleaned_csv = st.file_uploader("Upload your cleaned CSV file", type=["csv"])
    if cleaned_csv is not None:
        st.write("Your cleaned CSV file has been uploaded.")
        cleaned_score = evaluate(cleaned_csv)[0]
        
        cleaned_score_normalized = cleaned_score / 100

        bar_color = color_gradient(cleaned_score_normalized)
        st.progress(cleaned_score_normalized)
        st.write(f"Your cleaned score is: {cleaned_score:.2f}")
        
        if cleaned_score >= 80:
            st.success(f"Your cleaned score is: **{cleaned_score}**. Excellent!")
        elif cleaned_score >= 60:
            st.info(f"Your cleaned score is: **{cleaned_score}**. Good!")
        else:
            st.warning(f"Your cleaned score is: **{cleaned_score}**. Needs improvement.")
        name = st.text_input("Enter your name for the leaderboard:")
        if name and st.button("Submit Score"):
            save_leaderboard(name, cleaned_score)
            st.success("Score submitted!")
    else:
        st.write("Please upload your cleaned CSV file.")
elif page == "Leaderboard":
    st.title("Score Project - Leaderboard")
    if os.path.exists("leaderboard.csv"):
        leaderboard = pd.read_csv("leaderboard.csv")
        st.table(leaderboard)
    else:
        st.write("Leaderboard is empty.")