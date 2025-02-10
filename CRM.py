# crm_app.py
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import sqlite3
from streamlit_extras.add_vertical_space import add_vertical_space

# Database setup
DB_FILE = "crm.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_customer(name, email, phone, notes):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, email, phone, notes) VALUES (?, ?, ?, ?)",
                   (name, email, phone, notes))
    conn.commit()
    conn.close()

def get_customers():
    conn = sqlite3.connect(DB_FILE)
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return customers_df

# Initialize database
init_db()

# App layout
st.set_page_config(page_title="CRM System", layout="wide", page_icon="📊")

# Sidebar for navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x50.png?text=CRM+System", use_column_width=True)  # Placeholder logo
    add_vertical_space(2)
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Login", "Dashboard", "Add Customer"],
        icons=["person-circle", "bar-chart-fill", "person-plus-fill"],
        menu_icon="grid-3x3-gap-fill",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "#007bff", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#007bff", "color": "white"},
        },
    )

# Login Page
if selected == "Login":
    st.title("🔒 User Login")
    
    with st.form(key="login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            user = authenticate_user(username, password)
            if user:
                st.success(f"Welcome back, {username}! 🎉")
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
            else:
                st.error("Invalid username or password. Please try again.")

# Dashboard Page
elif selected == "Dashboard":
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        st.title(f"📊 Dashboard - Welcome {st.session_state['username']}!")
        
        # Display customer data
        customers_df = get_customers()
        
        if not customers_df.empty:
            st.subheader("Customer Data Overview")
            
            # Styled dataframe display with Streamlit's new dataframe features
            st.dataframe(customers_df.style.format({"phone": "{:.0f}"}).highlight_max(axis=0), use_container_width=True)

            # Visualize data
            st.subheader("📈 Customer Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                chart_option = st.selectbox("Choose chart type:", ["Bar Chart", "Pie Chart"])
                
                if chart_option == "Bar Chart":
                    bar_data = customers_df['name'].value_counts()
                    st.bar_chart(bar_data)

                elif chart_option == "Pie Chart":
                    pie_data = customers_df['name'].value_counts()
                    pie_chart_fig = pie_data.plot.pie(autopct="%1.1f%%").get_figure()
                    st.pyplot(pie_chart_fig)

            with col2:
                # Show summary stats or key metrics
                total_customers = len(customers_df)
                unique_emails = len(customers_df['email'].unique())
                st.metric(label="Total Customers", value=total_customers)
                st.metric(label="Unique Emails", value=unique_emails)

        else:
            st.info("No customer data available. Please add some customers first.")
            
    else:
        st.error("Please log in to access the dashboard.")

# Add Customer Page
elif selected == "Add Customer":
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        st.title("➕ Add New Customer")
        
        with st.form(key="add_customer_form"):
            name = st.text_input("Name", placeholder="Enter full name")
            email = st.text_input("Email", placeholder="Enter email address")
            phone = st.text_input("Phone", placeholder="Enter phone number")
            notes = st.text_area("Notes", placeholder="Additional details about the customer...")
            
            submit_button = st.form_submit_button("Add Customer")
            
            if submit_button:
                add_customer(name, email, phone, notes)
                st.success(f"Customer '{name}' added successfully! 🎉")
                
                # Clear form fields after submission (optional)
                name, email, phone, notes = "", "", "", ""
                
    else:
        st.error("Please log in to add customers.")
