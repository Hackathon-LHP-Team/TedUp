# process database
import pandas as pd
import os

def user_chat_session():
    df1 = pd.read_csv('assets/Chats.csv')

    # get the text for prediction
    df2 = pd.read_csv('assets/temp.csv')
    np_df2 = df2.values
    np_df2 = np_df2[0].tolist()

    # We have to append the text
    index = len(df1.columns)
    df1[index] = np_df2
    df1.to_csv('assets/Chats.csv', index=False)
    print(df1)

    # we have to delete the temp file for later use
    os.remove('assets/temp.csv')
    
user_chat_session()