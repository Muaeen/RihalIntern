import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w')
s = '****************************************************************'

# Creating a DataFrame without explicit index
data_frame = pd.DataFrame({'first': [50,21], 'sec': [131, 2]})
logging.info(data_frame)
logging.info(s)

# Here, a DataFrame is created with an explicit index, providing labels for the rows
data_frame = pd.DataFrame({'first': [50,21], 'sec': [131, 2]},
                 index = ['product_1', 'product_2'])
logging.info(data_frame)
logging.info(s)

# Creating a simple Series, which is a one-dimensional array-like object
series = pd.Series([1,2,3,4,5])
logging.info(series)
logging.info(s)

# Creating a Series with an explicit index and a name
series = pd.Series([1,2,3,4,5], 
                   index= ['first', 'second', 'third', 'fourth', 'fifth'],
                   name= 'Product_A')
logging.info(series)
logging.info(s)


df = pd.read_csv('winemag-data-130k-v2.csv')
logging.info(df.head())

print(df.shape)

df = pd.read_csv('winemag-data-130k-v2.csv', index_col=0)
logging.info(df)
logging.info(s)

logging.info(df.country)