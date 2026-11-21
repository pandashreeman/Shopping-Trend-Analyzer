import pandas as pd
import random
from datetime import datetime, timedelta

# Make the dataset reproducible
random.seed(42)

# Sample customer names
names = [
    "Rahul", "Amit", "Priya", "Neha", "Rohan",
    "Karan", "Sneha", "Anjali", "Vishal", "Pooja",
    "Arjun", "Meera", "Sahil", "Riya", "Dev"
]

# Product categories and products
products = {
    "Electronics": ["Laptop", "Mobile", "Headphones", "Keyboard", "Mouse"],
    "Clothing": ["Shirt", "Jeans", "Jacket", "T-Shirt", "Shoes"],
    "Grocery": ["Rice", "Milk", "Oil", "Sugar", "Wheat"],
    "Beauty": ["Face Wash", "Perfume", "Shampoo", "Cream", "Soap"],
    "Furniture": ["Chair", "Table", "Sofa", "Bed", "Cupboard"]
}

# Product prices
prices = {
    "Laptop": 45000,
    "Mobile": 18000,
    "Headphones": 1500,
    "Keyboard": 800,
    "Mouse": 500,
    "Shirt": 900,
    "Jeans": 1600,
    "Jacket": 2500,
    "T-Shirt": 600,
    "Shoes": 2200,
    "Rice": 800,
    "Milk": 60,
    "Oil": 150,
    "Sugar": 50,
    "Wheat": 400,
    "Face Wash": 250,
    "Perfume": 1200,
    "Shampoo": 300,
    "Cream": 180,
    "Soap": 50,
    "Chair": 2500,
    "Table": 5000,
    "Sofa": 25000,
    "Bed": 18000,
    "Cupboard": 12000
}

payment_methods = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Cash",
    "Net Banking"
]

# Generate 10,000 shopping transactions
data = []

start_date = datetime(2025, 1, 1)

for i in range(1, 10001):

    customer_id = random.randint(1001, 1500)
    customer_name = random.choice(names)

    category = random.choice(list(products.keys()))
    product = random.choice(products[category])

    age = random.randint(18, 65)
    gender = random.choice(["Male", "Female"])

    quantity = random.randint(1, 5)

    purchase_amount = prices[product] * quantity

    payment_method = random.choice(payment_methods)

    purchase_date = start_date + timedelta(
        days=random.randint(0, 680)
    )

    data.append({
        "Transaction ID": i,
        "Customer ID": customer_id,
        "Customer Name": customer_name,
        "Age": age,
        "Gender": gender,
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "Purchase Amount": purchase_amount,
        "Payment Method": payment_method,
        "Purchase Date": purchase_date.strftime("%Y-%m-%d")
    })

# Convert data into DataFrame
df = pd.DataFrame(data)

# Save CSV file
df.to_csv("datasets/shopping_data.csv", index=False)

print("Dataset created successfully!")
print("Total Records:", len(df))
print("Total Columns:", len(df.columns))
print("\nDataset Preview:")
print(df.head())