# visualization
import plotly.express as px

# machine learning libs
import pandas as pd
import numpy as np
from score import score



df = pd.read_csv('assets/Chats.csv')
for i in range(len(df.columns)):
    
        Chats = df.iloc[:,i].tolist()
        
        # Create an object of the class
        score_obj = score(Chats)

        # Call the methods on the object
        tokenizer = score_obj.generate_token()
        padded_chat_seq = score_obj.tokenize_text(tokenizer)
        Q_res, s_res = score_obj.Q_value(padded_chat_seq)

        s_res = pd.DataFrame(s_res)
        print(s_res)
        fig = px.line(s_res, x=s_res.index, y="0")
        fig.show()
        print('-'*10)
