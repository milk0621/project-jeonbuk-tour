import pandas as pd

region_df = pd.read_csv("./datas/region.csv")

region_df.drop(columns="areacode", inplace=True)
region_df.drop(columns="booktour", inplace=True)
region_df.drop(columns="contenttypeid", inplace=True)
region_df.drop(columns="createdtime", inplace=True)
region_df.drop(columns="cpyrhtDivCd", inplace=True)
region_df.drop(columns="modifiedtime", inplace=True)
region_df.drop(columns="sigungucode", inplace=True)
region_df.drop(columns="tel", inplace=True)
region_df.drop(columns="zipcode", inplace=True)
region_df.drop(columns="addr2", inplace=True)
region_df.drop(columns="mlevel", inplace=True)
region_df.drop(columns="firstimage2", inplace=True)

region_post = pd.read_csv("./datas/tour_details.csv")

region_post.drop(columns="tel", inplace=True)
region_post.drop(columns="zipcode", inplace=True)

#병합
result = pd.merge( region_post, region_df, how='left', on='contentid')

#결측값 빈문자로 대체

print(result.info())

print(result.isnull().sum())

result.dropna(subset=["title"], inplace=True)

result.to_csv("./datas/pre_region_data.csv", index=False)
#인덱스 -> DB의 no