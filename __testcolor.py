import pandas as pd
import numpy as np

np.random.seed(24)
df = pd.DataFrame({'A': np.linspace(1, 10, 10)})
df = pd.concat([df, pd.DataFrame(np.random.RandomState(24).randn(10, 4), columns=list('BCDE'))], axis=1)
df.iloc[0, 2] = np.nan
print(df)

styled = df.style.applymap(lambda val: 'color: %s' % 'red' ).highlight_max()

styled.to_excel('styled.xlsx', engine='openpyxl')