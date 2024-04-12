import json
import pandas as pd

df1 = pd.read_pickle('df1.pkl', compression='zip')

with open('final_res_vectors.json', 'r') as vectors_file:
    vectors = json.load(vectors_file)

for ticker in vectors:
    for day in vectors[ticker]:
        #print(df1.loc[df1['time']==day])
        for i in range(0, 300):
        #for coord in vectors[ticker][day]:
            df1.loc[(df1['time'] == day) & (df1['ticker'] == ticker), 'v'+str(i)] = vectors[ticker][day][i]

pd.to_pickle(df1, 'final_res.pkl', compression='zip')

df2 = pd.read_pickle('final_res.pkl', compression='zip')
print(df2)





























#df1['mm'] = 'Null'
#test = ['2023-02-12','2024-02-13','2024-02-14','2024-02-15','2024-02-16']
#for day in test:
    #ssd = df1.iloc[1]
    #nf = df1.loc[df1['time']==day]
    #nf['mm'] = 'QQQQ'
    #print(df1.loc[(df1['time'] == day) & (df1'ticker' == 'LKOH')])
#    df1.loc[(df1['time'] == day) & (df1['ticker'] == 'LKOH'), 'mm'] = 'QQQ'
#df1.loc[1,'mm'] = 'AAA'
#print(df1)
#df1['0'] = 'Null'
#for i in df1:
#    print(i)
#ssd = df1.loc[df1['ticker']=='VKCO']
#df1['mm'] = 'Null'
#ssd = df1.iloc[1]
#ssd['mm'] = 'Super'
#df1.iloc[1] = ssd
#print(df1)