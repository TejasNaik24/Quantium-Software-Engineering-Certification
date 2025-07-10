import pandas as pd
import os

# Step 1: Load and combine all CSV files
data_dir = "data"
all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".csv")]
df_list = [pd.read_csv(file) for file in all_files]
data = pd.concat(df_list, ignore_index=True)

# Step 2: Clean price column
data['price'] = data['price'].replace('[\$,]', '', regex=True).astype(float)

# Step 3: Filter only 'pink morsel' product
pink_data = data[data['product'] == 'pink morsel'].copy()

# Step 4: Convert 'date' to datetime
pink_data['date'] = pd.to_datetime(pink_data['date'])

# Step 5: Split data before and after Jan 15, 2021
cutoff_date = pd.to_datetime("2021-01-15")
before = pink_data[pink_data['date'] < cutoff_date]
after = pink_data[pink_data['date'] >= cutoff_date]

# Step 6: Calculate total sales (price * quantity)
before_sales = (before['price'] * before['quantity']).sum()
after_sales = (after['price'] * after['quantity']).sum()

# Output results
print("Total sales BEFORE Jan 15, 2021: ${:,.2f}".format(before_sales))
print("Total sales AFTER Jan 15, 2021: ${:,.2f}".format(after_sales))

# Optional: Write summary to a file
with open("pink_morsel_sales_summary.txt", "w") as f:
    f.write("Total sales BEFORE Jan 15, 2021: ${:,.2f}\n".format(before_sales))
    f.write("Total sales AFTER Jan 15, 2021: ${:,.2f}\n".format(after_sales))
