import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('outtable.csv')

# Filter for rows where the 3rd column has a value of 1
filtered_df = df[df.iloc[:, 2] == 1]

# Print the filtered DataFrame
print(filtered_df)

