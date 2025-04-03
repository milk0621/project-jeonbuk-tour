import pandas as pd
import re

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

result.dropna(subset=["title"], inplace=True)

def cleanhtml(text):
    text = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    if text:  
        return text[0]
    else :
        return ""
    
result["homepage"] = result["homepage"].fillna("")

result["homepage"] = result["homepage"].astype(str).apply(cleanhtml)

result["firstimage"] = result["firstimage"].fillna("https://cdn-icons-png.flaticon.com/512/1174/1174795.png")

result["sigungu"] = result["addr1"].str[8:11]

result.to_csv("./datas/pre_region_data.csv", index=False)
#인덱스 -> DB의 no