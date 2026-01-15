import streamlit as st
from datetime import datetime
import database as db

def show_employee_management():
    """Employee Management Section"""
    st.header("Employee Management")
    
    tab1, tab2 = st.tabs(["Add Employee", "View Employees"])
    
    with tab1:
        st.subheader("Add New Employee")
        with st.form("add_employee_form"):
            name = st.text_input("Employee Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            submitted = st.form_submit_button("Add Employee")
            
            if submitted:
                if name:
                    success, message = db.add_employee(name, email, phone)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter employee name")
    
    with tab2:
        employees = db.get_all_employees()
        if employees:
            st.write("**Current Employees:**")
            for emp in employees:
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    st.write(emp)
                with col2:
                    if st.button("🗑️", key=f"del_emp_{emp}"):
                        db.delete_employee(emp)
                        st.success(f"Deleted {emp}")
                        st.rerun()
        else:
            st.info("No employees added yet")


def show_customer_management():
    """Customer Management Section"""
    st.header("Customer Management")
    
    tab1, tab2, tab3 = st.tabs(["Add Customer", "View Customers", "Edit Customer"])
    
    with tab1:
        st.subheader("Add New Customer")
        with st.form("add_customer_form"):
            name = st.text_input("Customer Name")
            contact_person = st.text_input("Contact Person")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            submitted = st.form_submit_button("Add Customer")
            
            if submitted:
                if name:
                    success, message = db.add_customer(name, contact_person, email, phone, address)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter customer name")
    
    with tab2:
        customers = db.get_all_customers()
        if customers:
            st.write("**Current Customers:**")
            for cust in customers:
                st.write(f"• {cust}")
        else:
            st.info("No customers added yet")
    
    with tab3:
        st.subheader("Edit Customer Information")
        customers = db.get_all_customers()
        if customers:
            selected_customer = st.selectbox("Select Customer to Edit", customers)
            customer_details = db.get_customer_details(selected_customer)
            
            with st.form("edit_customer_form"):
                contact_person = st.text_input("Contact Person", value=customer_details.get("contact_person", ""))
                email = st.text_input("Email", value=customer_details.get("email", ""))
                phone = st.text_input("Phone", value=customer_details.get("phone", ""))
                address = st.text_area("Address", value=customer_details.get("address", ""))
                submitted = st.form_submit_button("Update Customer")
                
                if submitted:
                    success, message = db.update_customer(selected_customer, contact_person, email, phone, address)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.info("No customers available")


def show_project_category_management():
    """Project Category Management Section"""
    st.header("Project Category Management")
    
    st.subheader("Available Project Categories")
    categories = db.get_all_project_categories()
    for cat in categories:
        st.write(f"• {cat}")
    
    st.info("Project categories are predefined: EPC, ISS, PSE, SPP")


if __name__ == "__main__":
    # Initialize database
    db.init_database()
    
    st.set_page_config(page_title="CRM Master Data", layout="wide")
    st.title("CRM - Master Data Management")
    
    tab1, tab2, tab3 = st.tabs(["Employees", "Customers", "Project Categories"])
    
    with tab1:
        show_employee_management()
    
    with tab2:
        show_customer_management()
    
    with tab3:
        show_project_category_management()
