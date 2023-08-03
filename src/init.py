import pandas as pd

def init():
    temp = ["init"]
    temp = pd.DataFrame(temp)
    temp.to_csv('assets/temp.csv', index=False)
    
init()