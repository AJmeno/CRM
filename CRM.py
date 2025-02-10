import streamlit as st
import pandas as pd

# Initialize session state for customer and project data
if "customer_data" not in st.session_state:
    st.session_state["customer_data"] = pd.DataFrame(columns=["Name", "Email", "Phone", "Status"])

if "project_data" not in st.session_state:
    st.session_state["project_data"] = pd.DataFrame(
        columns=[
            "WBS Number", "Task Name", "WBS Description", "Must Start by Date",
            "Must End by Date", "Task Level of Effort (in hours)", 
            "Task Duration (in days)", "Predecessor (Finish-to-Start Dependency)",
            "Resource Name(s)", "Author", "Status", "Date Completed",
            "Planned Start Date", "Actual Start Date", "Reason for Delay/Issue"
        ]
    )

# App title
st.title("CRM and Project Management Dashboard")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Customer Management", "Project Management"])

# Customer Management Functions
def view_customers():
    st.subheader("Customer Data")
    if st.session_state["customer_data"].empty:
        st.write("No customer data available.")
    else:
        st.dataframe(st.session_state["customer_data"])

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
                updated_customer = {"Name": name, "Email": email, "Phone": phone, "Status": status}
                for key in updated_customer.keys():
                    st.session_state["customer_data"].at[customer_index, key] = updated_customer[key]
                st.success(f"Customer '{name}' updated successfully!")
            
            if delete_btn:
                st.session_state["customer_data"] = st.session_state["customer_data"].drop(customer_index).reset_index(drop=True)
                st.success(f"Customer '{selected_customer}' deleted successfully!")

# Project Management Functions
def view_projects():
    st.subheader("Project Data")
    if st.session_state["project_data"].empty:
        st.write("No project data available.")
    else:
        # Display project data as a table
        project_table = (
            st.session_state["project_data"]
            .sort_values(by=["WBS Number"])  # Sort by WBS Number for clarity
            .reset_index(drop=True)
        )
        st.dataframe(project_table)

def add_project_task():
    st.subheader("Add New Project Task")
    with st.form("add_project_task_form"):
        wbs_number = st.text_input("WBS Number")
        task_name = st.text_input("Task Name")
        wbs_description = st.text_area("WBS Description")
        must_start_by_date = st.date_input("Must Start by Date")
        must_end_by_date = st.date_input("Must End by Date")
        task_effort_hours = st.number_input("Task Level of Effort (in hours)", min_value=0, step=1)
        task_duration_days = st.number_input("Task Duration (in days)", min_value=0, step=1)
        predecessor_task = st.text_input("Predecessor (Finish-to-Start Dependency)")
        resource_names = st.text_area("Resource Name(s)")
        author_name = st.text_input("Author (for follow-on questions)")
        status_options = ["Not Started", "In-Process 50%", "Complete", "At Issue"]
        status = st.selectbox("Status", status_options)
        
        planned_start_date = must_start_by_date  # Default planned start date to start-by date
        actual_start_date = None  # Leave empty for now
        reason_for_delay_issue = ""

        submitted_task_form = st.form_submit_button("Add Task")

        if submitted_task_form:
            new_task = {
                "WBS Number": wbs_number,
                "Task Name": task_name,
                "WBS Description": wbs_description,
                "Must Start by Date": must_start_by_date,
                "Must End by Date": must_end_by_date,
                "Task Level of Effort (in hours)": task_effort_hours,
                "Task Duration (in days)": task_duration_days,
                "Predecessor (Finish-to-Start Dependency)": predecessor_task,
                "Resource Name(s)": resource_names,
                "Author": author_name,
                "Status": status,
                "Date Completed": None,
                "Planned Start Date": planned_start_date,
                "Actual Start Date": actual_start_date,
                "Reason for Delay/Issue": reason_for_delay_issue,
            }
            # Append new task to project data
            new_task_df = pd.DataFrame([new_task])
            new_task_df.index += len(st.session_state["project_data"])  # Update index
            # Add to session state
            new_project_df_all= pd.concat([st.session_state['project
