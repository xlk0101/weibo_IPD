import pandas as pd
from pandas import DataFrame
import numpy as np

df1 = DataFrame([1, 2, 3, 4])
df2 = DataFrame([4, 3, 2, 1])
print(df1.apply(sum).values)
print(np.abs(df1 - df2))
print(1 + df1 * 0.5 + df2 * 0.2)
