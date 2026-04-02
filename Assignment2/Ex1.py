#Read in a file from a url and save a local csv file with the first 10 rows

import pandas as pd
import numpy as np
import pyarrow

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

df = pd.read_csv(filename, engine='pyarrow')

out_file = "sales_data_test.csv"
df.head(10).to_csv(out_file, index=False)

