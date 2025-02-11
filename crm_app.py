# Import necessary libraries
import streamlit as st
import pandas as pd

# Initialize a simple database (in-memory)
if "customers" not in st.session_state:
    st.session_state["customers"] = pd.DataFrame(columns=["Customer ID", "Name", "Email", "Phone", "Notes"])

# Function to add a new customer
def add_customer(customer_id, name, email, phone, notes):
    new_customer = pd.DataFrame({
        "Customer ID": [customer_id],
        "Name": [name],
        "Email": [email],
        "Phone": [phone],
        "Notes": [notes]
    })
    st.session_state["customers"] = pd.concat([st.session_state["customers"], new_customer], ignore_index=True)

# Streamlit App Layout
st.title("CRM System")
st.markdown("By: Anthony Meno")
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Add Customer", "View Customers", "Search Customer"])

# Add Customer Section
if menu == "Add Customer":
    st.header("Add New Customer")
    with st.form("add_customer_form"):
        customer_id = st.text_input("Customer ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Customer")
        
        if submitted:
            add_customer(customer_id, name, email, phone, notes)
            st.success(f"Customer '{name}' added successfully!")

# View Customers Section
elif menu == "View Customers":
    st.header("Customer List")
    if not st.session_state["customers"].empty:
        st.dataframe(st.session_state["customers"])
    else:
        st.write("No customers added yet.")

# Search Customer Section
elif menu == "Search Customer":
    st.header("Search Customer")
    search_term = st.text_input("Enter Name or Email to search:")
    if search_term:
        results = st.session_state["customers"][
            (st.session_state["customers"]["Name"].str.contains(search_term, case=False)) |
            (st.session_state["customers"]["Email"].str.contains(search_term, case=False))
        ]
        if not results.empty:
            st.dataframe(results)
        else:
            st.write("No matching customers found.")
