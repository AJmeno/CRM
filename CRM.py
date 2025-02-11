import streamlit as st
import pandas as pd

# Load sample data
@st.cache_data
def load_data():
    return generate_sample_data()

data = load_data()

# App layout
st.title("Simulated CRM System")
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Dashboard", "Add Record", "Search Records"])

# Dashboard Page
if page == "Dashboard":
    st.header("CRM Dashboard")
    st.dataframe(data)
    st.write(f"Total Records: {len(data)}")

# Add Record Page
elif page == "Add Record":
    st.header("Add New Record")
    with st.form("add_record_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        status = st.selectbox("Status", ["Lead", "Contacted", "Customer"])
        submitted = st.form_submit_button("Submit")

        if submitted:
            new_record = {"Name": name, "Email": email, "Phone": phone, "Status": status}
            data = data.append(new_record, ignore_index=True)
            st.success("Record added successfully!")

# Search Records Page
elif page == "Search Records":
    st.header("Search Records")
    search_term = st.text_input("Search by Name or Email")
    if search_term:
        results = data[data["Name"].str.contains(search_term, case=False) | data["Email"].str.contains(search_term, case=False)]
        if not results.empty:
            st.dataframe(results)
        else:
            st.warning("No records found.")
