import pandas as pd
import numpy as np
def evaluate(csvfile):
    df = pd.read_csv(csvfile)
    duplicated = duplicated_score(df)
    columns_type = columns_type_score(df)
    isna = isna_score(df)
    date_s = evaluate_date_columns(df)
    l=[]
    if (duplicated<1):
        l.append("Duplicated Columns")
    if (columns_type<1):
        l.append("Columns Type")
    if (isna<1):
        l.append("Missing Values")
    if (date_s<1): 
        l.append("Date Columns")
    score = 0.2*duplicated + 0.1*columns_type + 0.5*isna + 0.2*date_s
    return score*100 , l
    
def duplicated_score(df):
   Number_duplicat = df.duplicated().sum()
   score = 1-Number_duplicat*2/(df.shape[0]-Number_duplicat)
   adj_score = np.square(score)
   return adj_score
def columns_type_score(df):
    object_columns = df.columns
    count = 0
    for col in object_columns:
        num_type = df[col].dropna().apply(type).nunique()
        if num_type != 1:
            count += 1
        score = 1-count/len(object_columns)
        adj_score = np.square(score)
    return adj_score
def isna_score(df):
    col_na = df.isna().any().sum()
    num_col =df.shape[1]
    score = 1 - col_na/num_col
    adj_score = np.square(score)
    return adj_score


from pandas.api.types import is_datetime64_any_dtype, is_object_dtype
from pandas.tseries.api import guess_datetime_format

def evaluate_date_columns(df, threshold=0.5):


    total_score = 0
    columns_evaluated = 0

    for col in df.columns:
        if is_datetime64_any_dtype(df[col]):
            total_score += 100   
            columns_evaluated += 1
            continue


        if is_object_dtype(df[col]):

            date_formats = df[col].apply(lambda x: guess_datetime_format(str(x)) if pd.notnull(x) else None)


            valid_date_count = date_formats.notnull().sum()
            total_count = len(df[col])


            if valid_date_count / total_count >= threshold:
                total_score += 50  
            else:
                total_score += 100  
            columns_evaluated += 1


    overall_score = (total_score / columns_evaluated) if columns_evaluated > 0 else 100

    return np.square((overall_score/100))