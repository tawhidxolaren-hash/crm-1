import streamlit as st
from datetime import datetime
import pandas as pd
import database as db

def show_all_leads():
    """Display all leads in a table"""
    st.header("All Leads")
    
    leads = db.get_all_leads()
    
    if leads:
        # Prepare data for display
        df_data = []
        for lead in leads:
            df_data.append({
                "ID": lead[0],
                "Customer": lead[1],
                "Category": lead[2],
                "Sales Person": lead[3],
                "Offer Date": lead[4],
                "Status": lead[5],
                "Initial Offer #": lead[6],
                "Revision": lead[7],
                "Priority": lead[8],
                "Follow-up Date": lead[9],
                "Next Follow-up": lead[10],
                "Serial Number": lead[11]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Allow selection and editing
        selected_id = st.selectbox("Select a lead to view/edit details", [lead[0] for lead in leads])
        
        if selected_id:
            show_lead_details(selected_id)
    else:
        st.info("No leads found. Create a new lead to get started.")


def show_lead_details(lead_id):
    """Display and allow editing of lead details"""
    lead = db.get_lead_by_id(lead_id)
    
    if lead:
        st.divider()
        st.subheader(f"Lead Details - ID: {lead_id}")
        
        # Convert lead tuple to dictionary for easier access
        lead_dict = {
            "id": lead[0],
            "customer_id": lead[1],
            "project_category": lead[2],
            "assigned_sales_person": lead[3],
            "offer_created": lead[4],
            "lead_through": lead[5],
            "scope_of_work": lead[6],
            "status": lead[7],
            "initial_offer_number": lead[8],
            "offer_revision_number": lead[9],
            "offered_value": lead[10],
            "priority": lead[11],
            "follow_up_by": lead[12],
            "follow_up_status": lead[13],
            "follow_up_date": lead[14],
            "next_follow_up_date": lead[15],
            "serial_number": lead[16],
            "customer_name": lead[-1]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Customer:** {lead_dict['customer_name']}")
            st.write(f"**Project Category:** {lead_dict['project_category']}")
            st.write(f"**Assigned Sales Person:** {lead_dict['assigned_sales_person']}")
            st.write(f"**Lead Through:** {lead_dict['lead_through']}")
            st.write(f"**Scope of Work:** {lead_dict['scope_of_work']}")
        
        with col2:
            st.write(f"**Status:** {lead_dict['status']}")
            st.write(f"**Initial Offer #:** {lead_dict['initial_offer_number']}")
            st.write(f"**Offer Revision:** {lead_dict['offer_revision_number']}")
            st.write(f"**Offered Value (BDT):** {lead_dict['offered_value']}")
            st.write(f"**Priority:** {lead_dict['priority']}")
        
        st.divider()
        st.subheader("Follow-up Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**Follow-up By:** {lead_dict['follow_up_by']}")
            st.write(f"**Follow-up Status:** {lead_dict['follow_up_status']}")
        
        with col2:
            st.write(f"**Follow-up Date:** {lead_dict['follow_up_date']}")
        
        with col3:
            st.write(f"**Next Follow-up Date:** {lead_dict['next_follow_up_date']}")
        
        if lead_dict['serial_number']:
            st.info(f"**Serial Number:** {lead_dict['serial_number']}")
        
        # Edit form
        st.divider()
        st.subheader("Update Lead")
        
        employees = db.get_all_employees()
        statuses = ["Connected", "Technical Analysis", "Price Offered", "Won", "Completed", "Lost"]
        priorities = ["P-1", "P-2", "P-3", "P-4"]
        
        with st.form("edit_lead_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_status = st.selectbox(
                    "Update Status",
                    statuses,
                    index=statuses.index(lead_dict['status']) if lead_dict['status'] in statuses else 0
                )
                new_priority = st.selectbox(
                    "Update Priority",
                    priorities,
                    index=priorities.index(lead_dict['priority']) if lead_dict['priority'] in priorities else 0
                )
            
            with col2:
                new_offered_value = st.number_input(
                    "Update Offered Value (BDT)",
                    value=lead_dict['offered_value'] if lead_dict['offered_value'] else 0.0,
                    min_value=0.0
                )
                new_follow_up_by = st.selectbox(
                    "Update Follow-up By",
                    employees if employees else ["No employees"],
                    index=employees.index(lead_dict['follow_up_by']) if lead_dict['follow_up_by'] in employees else 0
                )
            
            new_follow_up_status = st.text_input(
                "Update Follow-up Status",
                value=lead_dict['follow_up_status'] if lead_dict['follow_up_status'] else ""
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_follow_up_date = st.date_input(
                    "Update Follow-up Date",
                    value=datetime.strptime(lead_dict['follow_up_date'], '%Y-%m-%d').date() if lead_dict['follow_up_date'] else None
                )
            
            with col2:
                new_next_follow_up_date = st.date_input(
                    "Update Next Follow-up Date",
                    value=datetime.strptime(lead_dict['next_follow_up_date'], '%Y-%m-%d').date() if lead_dict['next_follow_up_date'] else None
                )
            
            submitted = st.form_submit_button("Update Lead", type="primary")
            
            if submitted:
                # Check if status changed to "Price Offered" and generate serial number
                new_serial_number = lead_dict['serial_number']
                if new_status == "Price Offered" and lead_dict['status'] != "Price Offered" and not new_serial_number:
                    new_serial_number = db.generate_serial_number(
                        lead_dict['project_category'],
                        lead_dict['customer_name'],
                        datetime.strptime(lead_dict['offer_created'], '%Y-%m-%d').date(),
                        lead_dict['initial_offer_number'],
                        lead_dict['offer_revision_number']
                    )
                
                success, message = db.update_lead(
                    lead_id,
                    status=new_status,
                    priority=new_priority,
                    offered_value=new_offered_value,
                    follow_up_by=new_follow_up_by,
                    follow_up_status=new_follow_up_status,
                    follow_up_date=new_follow_up_date,
                    next_follow_up_date=new_next_follow_up_date,
                    serial_number=new_serial_number
                )
                
                if success:
                    st.success("Lead updated successfully!")
                    st.rerun()
                else:
                    st.error(f"Error: {message}")


def show_leads_by_status():
    """Display leads grouped by status"""
    st.header("Leads by Status")
    
    statuses = ["Connected", "Technical Analysis", "Price Offered", "Won", "Completed", "Lost"]
    selected_status = st.selectbox("Select Status", statuses)
    
    leads = db.get_leads_by_status(selected_status)
    
    if leads:
        df_data = []
        for lead in leads:
            df_data.append({
                "ID": lead[0],
                "Customer": lead[1],
                "Category": lead[2],
                "Sales Person": lead[3],
                "Offer Date": lead[4],
                "Priority": lead[8],
                "Follow-up Date": lead[9],
                "Serial Number": lead[11]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f"No leads with status: {selected_status}")


def show_followup_reminders():
    """Display leads needing follow-up"""
    st.header("Follow-up Reminders")
    
    today = datetime.today().date()
    leads = db.get_leads_needing_followup(today)
    
    if leads:
        st.warning(f"**{len(leads)} leads need follow-up today or earlier!**")
        
        df_data = []
        for lead in leads:
            df_data.append({
                "ID": lead[0],
                "Customer": lead[1],
                "Category": lead[2],
                "Sales Person": lead[3],
                "Status": lead[5],
                "Follow-up Date": lead[6],
                "Next Follow-up": lead[7]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.success("No leads needing follow-up")


if __name__ == "__main__":
    # Initialize database
    db.init_database()
    
    st.set_page_config(page_title="CRM - Lead Tracking", layout="wide")
    st.title("CRM - Lead Tracking & Follow-ups")
    
    tab1, tab2, tab3, tab4 = st.tabs(["All Leads", "Leads by Status", "Follow-up Reminders", "Edit Lead"])
    
    with tab1:
        show_all_leads()
    
    with tab2:
        show_leads_by_status()
    
    with tab3:
        show_followup_reminders()
    
    with tab4:
        st.subheader("Edit Specific Lead")
        leads = db.get_all_leads()
        if leads:
            selected_id = st.selectbox(
                "Select Lead to Edit",
                [lead[0] for lead in leads],
                format_func=lambda x: f"ID {x} - {[l[1] for l in leads if l[0] == x][0]}"
            )
            show_lead_details(selected_id)
        else:
            st.info("No leads available")
