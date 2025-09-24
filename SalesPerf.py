import pandas as pd

df = pd.read_excel("data/Online Retail.xlsx")

print("Data Info:")
print(df.info())

print("\nFirst 5 Rows:")
print(df.head())

print("\nSummary:")
print(df.describe())

print("\nColumns:")
print(df.columns)

print(f"\nShape: {df.shape[0]} rows and {df.shape[1]} columns")

df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
print("\nTotalPrice column added.")

#Data Cleaning

print(df.isnull().sum())
df = df.dropna(subset=['CustomerID'])
df = df.drop_duplicates()
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')
df['Hour'] = df['InvoiceDate'].dt.hour
df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()

df.to_csv("data/cleaned_sales_data.csv", index=False)

#EDA

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/cleaned_sales_data.csv')

#top selling products
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
print("Top-Selling Products:\n", top_products)

plt.figure(figsize=(12,6))
top_products.plot(kind='barh', color='skyblue')
plt.title('Top 10 Best-Selling Products')
plt.xlabel('Total Quantity Sold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('visuals/top_products.png')
plt.show()

#Monthly Sales
df['InvoiceMonth'] = pd.to_datetime(df['InvoiceMonth'].astype(str))  # convert Period to datetime

monthly_sales = df.groupby('InvoiceMonth')['TotalPrice'].sum()

plt.figure(figsize=(12,6))
monthly_sales.plot(marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales (£)')
plt.grid(True)
plt.savefig('visuals/monthly_sales_trend.png')
plt.show()

#Hourly Sales
hourly_sales = df.groupby('Hour')['TotalPrice'].sum()

plt.figure(figsize=(10,5))
sns.lineplot(x=hourly_sales.index, y=hourly_sales.values, marker='o')
plt.title('Sales Trend by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Total Sales (£)')
plt.grid(True)
plt.savefig('visuals/hourly_sales_trend.png')
plt.show()

#weekly sales
dow_sales = df.groupby('DayOfWeek')['TotalPrice'].sum().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

plt.figure(figsize=(10,5))
sns.barplot(x=dow_sales.index, y=dow_sales.values, palette='viridis')
plt.title('Total Sales by Day of Week')
plt.ylabel('Total Sales (£)')
plt.xticks(rotation=45)
plt.savefig('visuals/sales_by_day.png')
plt.show()

#knowing customers

print("Total Unique Customers:", df['CustomerID'].nunique())

#by revenue
top_customers = df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head(10)

top_customers.plot(kind='bar', color='orange')
plt.title('Top 10 Customers by Revenue')
plt.xlabel('Customer ID')
plt.ylabel('Total Revenue')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('visuals/top_cust_byRevenue.png')
plt.show()

#by quantity purchased
top_qty_customers = df.groupby('CustomerID')['Quantity'].sum().sort_values(ascending=False).head(10)

top_qty_customers.plot(kind='bar', color='skyblue')
plt.title('Top 10 Customers by Quantity')
plt.xlabel('Customer ID')
plt.ylabel('Total Quantity')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('visuals/top_cust_byQuantity.png')
plt.show()

#avg spend per customer
avg_spend = df.groupby('CustomerID')['TotalPrice'].sum().mean()
print("Average Revenue per Customer: ", round(avg_spend, 2))

#RFM segmentation
import datetime
snapshot_date = df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])


rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalPrice': 'sum'
}).rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
})

rfm.head()

print("Segment Distribution:")
print(rfm['Segment'].value_counts())

# Pie chart 
rfm['Segment'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, figsize=(8,8), colormap='Set3')
plt.title("Customer Segment Distribution")
plt.ylabel("")  # hides the y-axis label
plt.savefig("visuals/segment_pie_chart.png")
plt.show()

segment_summary = rfm.groupby('Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count']
}).round(1)

print(segment_summary)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
sns.countplot(data=rfm, x='Segment', order=rfm['Segment'].value_counts().index, palette='Set2')
plt.title('Customer Segments Distribution')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visuals/segment_count_bar.png")
plt.show()

