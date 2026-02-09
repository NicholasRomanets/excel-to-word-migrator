import pandas as pd

df = pd.read_excel("Source.xlsx", sheet_name="first", usecols=[5,6,7,2,3,22,21,18,16,4,14,23,24])

print(df)
df = df.dtypes
print(df)