import pandas as pd
import re

df = pd.read_csv("./datas/review_data.csv")
df2 = pd.read_csv("./datas/csv/pre_region_data.csv")

result = pd.merge(df2, df, how='left', on='title')


text = result["review"]
def clean(text):
    text = text.replace("\r", " ").replace("\n", " ")
    if text:
        return text
    else:
        return ""

result.drop(columns=["title", "overview", "homepage", "addr1", "cat1", "cat2", "cat3", "firstimage", "mapx", "mapy", "sigungu"], inplace=True)

result["review"] = text.fillna("").apply(clean)
result.to_csv("./datas/csv/pre_review.csv", index=False)


# df = pd.read_csv("./datas/pre_review.csv")
# df.drop(columns=["name", "score", "total_score"], inplace=True)
# print(df)
# print("=" *50)
# # dfs = df.groupby("title")


# dfs = (df.groupby(["title"]).sum().reset_index())
# print(dfs)
# dfs.to_csv("./datas/review_groub.csv", index=False)