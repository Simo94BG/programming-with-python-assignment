import pandas as pd

list1 = [1, 2, 5, 8]
list2 = [3, 5, 9, 13]
df1 = pd.DataFrame(list1, columns=['x'])
df2 = pd.DataFrame(list2, columns=['x'])
diff_squared = (df1['x'] - df2['x'])**1
print(diff_squared)
sse = sum(diff_squared**2)
print(sse)