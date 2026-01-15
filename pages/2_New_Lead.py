import streamlit as st
from datetime import datetime
import database as db

def show_new_lead_form():
    """Display the lead creation form"""
    st.header("New Lead Entry")
    
    # Get reference data
    employees = db.get_all_employees()
    customers = db.get_all_customers()
    categories = db.get_all_project_categories()
    statuses = ["Connected", "Technical Analysis", "Price Offered", "Won", "Completed", "Lost"]
    priorities = ["P-1", "P-2", "P-3", "P-4"]
    
    with st.form("new_lead_form", border=False):
        st.subheader("Customer & Project Information")
        
        # Two column layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer selection with option to add new
            customer_selection = st.radio("Customer Selection", ["Select Existing", "Add New"])
            
            if customer_selection == "Select Existing":
                if customers:
                    customer_name = st.selectbox("Customer Name", customers)
                else:
                    st.error("No customers found. Please add customers in Master Data first.")
                    customer_name = None
            else:
                customer_name = st.text_input("New Customer Name")
                contact_person = st.text_input("Contact Person")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                address = st.text_area("Address", height=80)
        
        with col2:
            project_category = st.selectbox("Project Category", categories)
        
        st.divider()
        st.subheader("Offer & Sales Information")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            assigned_sales_person = st.selectbox("Assigned Sales Person", employees if employees else ["No employees"])
        
        with col2:
            offer_created = st.date_input("Offer Created", value=datetime.today())
        
        with col3:
            lead_through = st.selectbox("Lead Through", employees if employees else ["No employees"], key="lead_through")
        
        with col4:
            scope_of_work = st.text_input("Scope of Work")
        
        st.divider()
        st.subheader("Offer Details")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status = st.selectbox("Status", statuses)
        
        with col2:
            # Initial offer number will be auto-calculated if customer and category are selected
            initial_offer_number_display = st.empty()
            
        with col3:
            # Offer revision will be auto-calculated
            offer_revision_display = st.empty()
        
        with col4:
            offered_value = st.number_input("Offered Value (BDT)", min_value=0.0, value=0.0)
        
        st.divider()
        st.subheader("Priority & Follow-up")
        
        col1, col2 = st.columns(2)
        
        with col1:
            priority = st.selectbox("Priority", priorities)
        
        with col2:
            follow_up_by = st.selectbox("Follow-up By", employees if employees else ["No employees"], key="follow_up_by")
        
        follow_up_status = st.text_input("Follow-up Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            follow_up_date = st.date_input("Follow-up Date", value=None)
        
        with col2:
            next_follow_up_date = st.date_input("Next Follow-up Date", value=None)
        
        # Submit button
        submitted = st.form_submit_button("Create Lead", use_container_width=True, type="primary")
    
    if submitted:
        # Validate inputs
        validation_errors = []
        
        if not customer_name:
            validation_errors.append("Customer name is required")
        
        if customer_selection == "Add New" and not customer_name:
            validation_errors.append("Please enter a new customer name")
        
        if not assigned_sales_person or assigned_sales_person == "No employees":
            validation_errors.append("Assigned Sales Person is required. Please add employees first.")
        
        if not lead_through or lead_through == "No employees":
            validation_errors.append("Lead Through is required. Please add employees first.")
        
        if not follow_up_by or follow_up_by == "No employees":
            validation_errors.append("Follow-up By is required. Please add employees first.")
        
        if validation_errors:
            for error in validation_errors:
                st.error(error)
        else:
            # If adding new customer, add it first
            if customer_selection == "Add New":
                success, message = db.add_customer(customer_name, contact_person, email, phone, address)
                if not success:
                    st.error(f"Could not add customer: {message}")
                    return
            
            # Get customer ID
            customer_id = db.get_customer_id(customer_name)
            
            # Calculate offer numbers
            initial_offer_number = db.get_next_initial_offer_number(customer_name, project_category)
            offer_revision_number = db.get_next_offer_revision_number(customer_name, project_category, initial_offer_number)
            
            # Generate serial number if status is "Price Offered"
            serial_number = None
            if status == "Price Offered":
                serial_number = db.generate_serial_number(
                    project_category, customer_name, offer_created,
                    initial_offer_number, offer_revision_number
                )
            
            # Add lead
            success, message = db.add_lead(
                customer_id=customer_id,
                project_category=project_category,
                assigned_sales_person=assigned_sales_person,
                offer_created=offer_created,
                lead_through=lead_through,
                scope_of_work=scope_of_work,
                status=status,
                initial_offer_number=initial_offer_number,
                offer_revision_number=offer_revision_number,
                offered_value=offered_value,
                priority=priority,
                follow_up_by=follow_up_by,
                follow_up_status=follow_up_status,
                follow_up_date=follow_up_date,
                next_follow_up_date=next_follow_up_date,
                serial_number=serial_number
            )
            
            if success:
                st.success(f"Lead created successfully! Serial Number: {serial_number if serial_number else 'N/A'}")
                st.balloons()
                st.rerun()
            else:
                st.error(f"Error creating lead: {message}")


if __name__ == "__main__":
    # Initialize database
    db.init_database()
    
    st.set_page_config(page_title="CRM - New Lead", layout="wide")
    st.title("CRM - Lead Management")
    
    show_new_lead_form()
