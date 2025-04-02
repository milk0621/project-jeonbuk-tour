import re
import pandas as pd

region_df = pd.read_csv("./datas/pre_region_data.csv")

def cleanhtml(text):
    text = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    if text:  
        return text[0]
    else :
        return ""
    
region_df["homepage"] = region_df["homepage"].fillna("")

region_df["homepage"] = region_df["homepage"].astype(str).apply(cleanhtml)

print(region_df["homepage"])