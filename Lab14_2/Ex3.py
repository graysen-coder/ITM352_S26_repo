import matplotlib.pyplot as plt
import pandas as pd

trips_df = pd.read_json("..trips from area 8.json")

trips_df = trips_df[["tips", "payment_type"]]

trips_df = trips_df.dropna()
trips_df = trips_df.estype({"tips": "float"})
trips_df = trips_df.set_index("payment_type")

tips_by_payment = trips_df.groupby("payment_type").sum()

x_labels = pd.Series(tips_by_payment.index.values)
y_values = pd.Series(tips_by_payment["tips"].values)



plt.show()