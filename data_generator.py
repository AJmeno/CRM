import pandas as pd
import numpy as np

# Generate sample data
def generate_sample_data():
    data = {
        "Name": [f"Person {i}" for i in range(1, 21)],
        "Email": [f"person{i}@example.com" for i in range(1, 21)],
        "Phone": [f"+123456789{i}" for i in range(1, 21)],
        "Status": np.random.choice(["Lead", "Contacted", "Customer"], size=20),
        "Last Interaction": pd.date_range("2025-01-01", periods=20).strftime("%Y-%m-%d").tolist(),
    }
    return pd.DataFrame(data)

sample_data = generate_sample_data()
