import pandas as pd

df = pd.read_csv("./datas/pre_region_data.csv")

print(df[df["title"] == "남원 추어마을"])