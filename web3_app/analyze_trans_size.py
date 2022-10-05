import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('trans_ave_size_3.csv')
print(np.mean(df['Ave._Transaction_Size']))

plt.plot(df['block_number'], df['Ave._Transaction_Size'])
plt.title('Ave. Transaction Size per Block')
plt.xlabel('Block Number')
plt.ylabel('Ave. Transaction Size')
plt.xticks(rotation='vertical')
plt.show()