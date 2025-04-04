import pandas as pd

df = pd.read_csv("./datas/pre_region_data.csv")

print(df[df["title"] == "농업회사법인 주식회사 공동체공간 수작"])