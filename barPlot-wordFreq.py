import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

db=pd.read_excel("latestResult.xlsx",sheet_name="raw_data")
#print(db)
db_entries=db.drop_duplicates().count()
#db_keyword=db.groupby(db['Item'])

db_keyword.first()

%matplotlib inline
plt.figure(figsize=(40,40))
plt.xticks(rotation=50)
plt.tick_params(labelsize=18)
plt.bar(db['Item'],np.log10(db['Frequency']))
plt.show()