import streamlit as st
import database as db
from datetime import datetime

def main():
    st.set_page_config(
        page_title="CRM System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize database
    db.init_database()
    
    st.title("📊 CRM Management System")
    st.markdown("""
    Welcome to the CRM System for managing leads and customer relationships.
    
    **Features:**
    - 📋 Master Data Management (Employees, Customers, Projects)
    - 🆕 Create and track new leads
    - 📈 Monitor lead status and progress
    - 📞 Manage follow-ups and reminders
    - 🏷️ Auto-generate serial numbers for offers
    
    Use the sidebar to navigate between different sections.
    """)
    
    st.divider()
    
    # Dashboard overview
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Get overview statistics
        all_leads = db.get_all_leads()
        all_employees = db.get_all_employees()
        all_customers = db.get_all_customers()
        
        connected_leads = db.get_leads_by_status("Connected")
        technical_leads = db.get_leads_by_status("Technical Analysis")
        price_offered_leads = db.get_leads_by_status("Price Offered")
        won_leads = db.get_leads_by_status("Won")
        
        with col1:
            st.metric("Total Leads", len(all_leads))
        
        with col2:
            st.metric("Total Customers", len(all_customers))
        
        with col3:
            st.metric("Total Employees", len(all_employees))
        
        with col4:
            st.metric("Won Deals", len(won_leads))
    except:
        st.warning("Please ensure master data is set up first")
    
    st.divider()
    
    # Quick summary
    col1, col2, col3 = st.columns(3)
    
    try:
        with col1:
            st.subheader("Lead Status Summary")
            st.write(f"🔗 Connected: {len(connected_leads)}")
            st.write(f"🔍 Technical Analysis: {len(technical_leads)}")
            st.write(f"💰 Price Offered: {len(price_offered_leads)}")
            st.write(f"✅ Won: {len(won_leads)}")
        
        with col2:
            st.subheader("Quick Actions")
            if st.button("➕ New Lead", use_container_width=True):
                st.info("Go to 'New Lead' in the sidebar")
            if st.button("⚙️ Master Data", use_container_width=True):
                st.info("Go to 'Master Data' in the sidebar")
            if st.button("📊 View All Leads", use_container_width=True):
                st.info("Go to 'Lead Tracking' in the sidebar")
        
        with col3:
            st.subheader("Upcoming Follow-ups")
            today = datetime.today().date()
            followup_leads = db.get_leads_needing_followup(today)
            if followup_leads:
                st.warning(f"⚠️ {len(followup_leads)} leads need follow-up")
                for lead in followup_leads[:5]:
                    st.write(f"• {lead[1]} - {lead[6]}")
                if len(followup_leads) > 5:
                    st.write(f"... and {len(followup_leads) - 5} more")
            else:
                st.success("✅ No pending follow-ups")
    except:
        pass
    
    st.divider()
    
    st.subheader("System Information")
    st.markdown("""
    **Navigation:**
    1. **Master Data** - Set up employees, customers, and projects
    2. **New Lead** - Create new leads and opportunities
    3. **Lead Tracking** - Monitor and update lead status and follow-ups
    
    **Key Features:**
    - Automatic serial number generation for offers (XBL format)
    - Offer revision tracking (R1, R2, R3...)
    - Follow-up reminders and scheduling
    - Priority and status management
    
    For support or questions, contact your administrator.
    """)


if __name__ == "__main__":
    main()
