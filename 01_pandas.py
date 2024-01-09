import pandas as pd

# Creating a DataFrame without explicit index
data_frame = pd.DataFrame({'first': [50,21], 'sec': [131, 2]})
print(data_frame)
print('****************************************************************')

# Here, a DataFrame is created with an explicit index, providing labels for the rows
data_frame = pd.DataFrame({'first': [50,21], 'sec': [131, 2]},
                 index = ['product_1', 'product_2'])
print(data_frame)
print('****************************************************************')

# Creating a simple Series, which is a one-dimensional array-like object
series = pd.Series([1,2,3,4,5])
print(series)
print('****************************************************************')

# Creating a Series with an explicit index and a name
series = pd.Series([1,2,3,4,5], 
                   index= ['first', 'second', 'third', 'fourth', 'fifth'],
                   name= 'Product_A')
print(series)
print('****************************************************************')
