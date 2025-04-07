import pandas as pd
import re

# df = pd.read_csv("./datas/review_data.csv")

# text = df["review"]
# def clean(text):
#     text = text.replace("\r", " ").replace("\n", " ")
#     if text:
#         return text
#     else:
#         return ""

# df["review"] = text.fillna("").apply(clean)
# df.to_csv("./datas/pre_review.csv", index=False)


df = pd.read_csv("./datas/pre_review.csv")
df.drop(columns=["name", "score", "total_score"], inplace=True)
print(df)
print("=" *50)
# dfs = df.groupby("title")


dfs = (df.groupby(["title"]).sum().reset_index())
print(dfs)
dfs.to_csv("./datas/review_groub.csv", index=False)