import streamlit as st
import pandas as pd

# Initialize session state for customer data
if "customer_data" not in st.session_state:
    st.session_state["customer_data"] = pd.DataFrame(columns=["Name", "Email", "Phone", "Status"])

# App title
st.title("CRM Dashboard")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["View Data", "Add Customer", "Edit/Delete Customer", "Analytics"])

# Function to display customer data
def view_data():
    st.subheader("Customer Data")
    if st.session_state["customer_data"].empty:
        st.write("No customer data available.")
    else:
        st.dataframe(st.session_state["customer_data"])

# Function to add a new customer
def add_customer():
    st.subheader("Add New Customer")
    with st.form("add_customer_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        status = st.selectbox("Status", ["Active", "Inactive"])
        submitted = st.form_submit_button("Add Customer")
        
        if submitted:
            new_customer = {"Name": name, "Email": email, "Phone": phone, "Status": status}
            st.session_state["customer_data"] = pd.concat(
                [st.session_state["customer_data"], pd.DataFrame([new_customer])], ignore_index=True
            )
            st.success("Customer added successfully!")

# Function to edit or delete customers
def edit_delete_customer():
    st.subheader("Edit/Delete Customer")
    if st.session_state["customer_data"].empty:
        st.write("No customer data available.")
        return
    
    customer_list = st.session_state["customer_data"]["Name"].tolist()
    selected_customer = st.selectbox("Select Customer to Edit/Delete", customer_list)
    
    if selected_customer:
        customer_index = st.session_state["customer_data"][st.session_state["customer_data"]["Name"] == selected_customer].index[0]
        
        with st.form("edit_delete_form"):
            name = st.text_input("Name", value=st.session_state["customer_data"].iloc[customer_index]["Name"])
            email = st.text_input("Email", value=st.session_state["customer_data"].iloc[customer_index]["Email"])
            phone = st.text_input("Phone", value=st.session_state["customer_data"].iloc[customer_index]["Phone"])
            status = st.selectbox(
                "Status",
                ["Active", "Inactive"],
                index=["Active", "Inactive"].index(st.session_state["customer_data"].iloc[customer_index]["Status"])
            )
            
            col1, col2 = st.columns(2)
            with col1:
                update_btn = st.form_submit_button("Update Customer")
            with col2:
                delete_btn = st.form_submit_button("Delete Customer")
            
            if update_btn:
                # Update customer details
                updated_customer = {"Name": name, "Email": email, "Phone": phone, "Status": status}
                for key in updated_customer.keys():
                    st.session_state["customer_data"].at[customer_index, key] = updated_customer[key]
                st.success(f"Customer '{name}' updated successfully!")
            
            if delete_btn:
                # Delete customer
                st.session_state["customer_data"] = st.session_state["customer_data"].drop(customer_index).reset_index(drop=True)
                st.success(f"Customer '{selected_customer}' deleted successfully!")

# Function to display analytics
def analytics():
    st.subheader("Customer Analytics")
    if st.session_state["customer_data"].empty:
        st.write("No data available for analytics.")
        return
    
    status_counts = st.session_state["customer_data"]["Status"].value_counts()
    st.bar_chart(status_counts)

# Menu navigation logic
if menu == "View Data":
    view_data()
elif menu == "Add Customer":
    add_customer()
elif menu == "Edit/Delete Customer":
    edit_delete_customer()
elif menu == "Analytics":
    analytics()
