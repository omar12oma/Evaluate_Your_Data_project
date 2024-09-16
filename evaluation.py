import pandas as pd
import numpy as np
def evaluate(csvfile):
    df = pd.read_csv(csvfile)
    duplicated = duplicated_score(df)
    columns_type = columns_type_score(df)
    isna = isna_score(df)
    l=[]
    if (duplicated<1):
        l.append("Duplicated Columns")
    if (columns_type<1):
        l.append("Columns Type")
    if (isna<1):
        l.append("Missing Values")
    score = 0.2*duplicated + 0.4*columns_type + 0.4*isna
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
def Evaluate_Your_Data(df):
    duplicated = duplicated_score(df)
    columns_type = columns_type_score(df)
    isna = isna_score(df)
    score = 0.2*duplicated + 0.4*columns_type + 0.4*isna
    return score*10