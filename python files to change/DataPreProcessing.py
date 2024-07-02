import pandas as pd

# to convert all csv file as per requirement (for csv file name= "daily_sales_data_0.csv")
df = pd.read_csv('daily_sales_data_0.csv')
df_pink = df[df['product']=='pink morsel']
df_pink.to_csv('daily_sales_data_0.csv')

df = pd.read_csv('daily_sales_data_0.csv')


# for the csv file name = "daily_sales_data_1.csv"
df1 = pd.read_csv('daily_sales_data_1.csv')
df_pink1 = df1[df1['product']=='pink morsel']
df_pink1.to_csv('daily_sales_data_1.csv')
print(df_pink1.to_string())

# for the csv file name = "daily_sales_data_2.csv"
df2 = pd.read_csv('daily_sales_data_2.csv')
df_pink2 = df2[df2['product']=='pink morsel']
df_pink2.to_csv('daily_sales_data_2.csv')
print(df_pink2.to_string())

# to concatenate all the three csv file in one csv file
csv_files = ['daily_sales_data_0.csv','daily_sales_data_1.csv','daily_sales_data_2.csv']
combined_df = pd.concat([pd.read_csv(file) for file in csv_files])
combined_df.to_csv('final_result.csv', index = False)
print("Combined CSV file created successfully")