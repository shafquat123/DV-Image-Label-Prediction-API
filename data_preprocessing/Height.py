import pandas as pd
data = pd.read_csv("C:\\Users\\dhrit\\Downloads\\pro_occurrences.csv")
df=pd.DataFrame(data)
#dataAvg=df.groupby('genus')
#dataAvg.mean().reset_index().to_csv(r'C://Users//dhrit//Downloads//DV//DVProject//avgheight.csv', index = None, header=True)

datacount=df.groupby(['year'])['id'].count()
datacount.reset_index().to_csv(r'C://Users//dhrit//Downloads//DV//DVProject//Code//yearcount.csv', index = None, header=True)

datacount=df.groupby(['institutionCode'])['id'].count()
datacount.reset_index().to_csv(r'C://Users//dhrit//Downloads//DV//DVProject//Code//institutioncount.csv', index = None, header=True)
