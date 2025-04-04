import pandas as pd

df = pd.read_csv("./datas/pre_region_data.csv")

print(df[df["title"] == "두여 정보화마을"])