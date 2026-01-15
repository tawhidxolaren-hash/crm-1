# CRM Management System

A simple yet powerful Customer Relationship Management (CRM) application built with Python and Streamlit for tracking leads, managing follow-ups, and maintaining customer relationships.

## Features

- **Master Data Management**
  - Employee management with contact details
  - Customer database with contact information
  - Project category management (EPC, ISS, PSE, SPP)

- **Lead Management**
  - Create new leads with comprehensive information
  - Track lead status throughout the sales pipeline
  - Automatic serial number generation

- **Offer Tracking**
  - Track multiple offers per customer
  - Automatic offer numbering (1, 2, 3...)
  - Revision tracking (R1, R2, R3...)

- **Follow-up Management**
  - Schedule follow-ups
  - Track follow-up status and notes
  - Reminders for overdue follow-ups

- **Serial Number Generation**
  - Automatic format: `XBL/<Project Category>/<Customer Name>/<Date>/<Offer Number>/<Revision>`
  - Generated when offer status becomes "Price Offered"

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crm-1
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
crm-1/
├── app.py                          # Main Streamlit application
├── database.py                     # Database initialization and operations
├── pages/
│   ├── 1_Master_Data.py           # Employee, Customer, Project management
│   ├── 2_New_Lead.py              # Lead creation form
│   └── 3_Lead_Tracking.py         # Lead tracking and follow-ups
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Database Schema

### Employees
- id, name, email, phone, created_at

### Customers
- id, name, contact_person, email, phone, address, created_at

### Project Categories
- Predefined: EPC, ISS, PSE, SPP

### Leads
- id, customer_id, project_category, assigned_sales_person
- offer_created, lead_through, scope_of_work
- status, initial_offer_number, offer_revision_number
- offered_value, priority
- follow_up_by, follow_up_status, follow_up_date, next_follow_up_date
- serial_number, created_at, updated_at

## Usage Guide

### 1. Master Data Setup
First, set up your master data:
- Go to **Master Data** page
- Add employees (sales team members)
- Add customers
- Edit customer information as needed

### 2. Creating a New Lead
- Navigate to **New Lead** page
- Fill in all required information:
  - Customer (existing or new)
  - Project category
  - Sales person assignment
  - Offer details
  - Priority and follow-up information
- Submit the form
- If status is "Price Offered", a serial number will be auto-generated

### 3. Tracking Leads
- Go to **Lead Tracking** page
- View all leads or filter by status
- Click on a lead to view/edit details
- Update status, priority, offered value, and follow-up dates
- Monitor follow-up reminders

### 4. Following Up
- Check **Follow-up Reminders** tab for overdue follow-ups
- Update follow-up status and schedule next follow-ups
- Track follow-up history

## Field Descriptions

### Lead Fields

| Field | Type | Description |
|-------|------|-------------|
| Project Category | Dropdown | EPC, ISS, PSE, SPP |
| Assigned Sales Person | Dropdown | Sales team member |
| Offer Created | Date | Date when offer was created |
| Lead Through | Dropdown | Source/referrer of the lead |
| Customer Name | Dropdown/Text | Existing or new customer |
| Scope of Work | Text | Description of the project scope |
| Status | Dropdown | Connected, Technical Analysis, Price Offered, Won, Completed, Lost |
| Initial Offer Number | Auto | Auto-incremented per customer/category |
| Offer Revision Number | Auto | R1, R2, R3... per offer number |
| Offered Value | Number | Amount in BDT |
| Priority | Dropdown | P-1 (highest) to P-4 (lowest) |
| Follow-up By | Dropdown | Assigned follow-up person |
| Follow-up Status | Text | Notes on follow-up progress |
| Follow-up Date | Date | Last follow-up date |
| Next Follow-up Date | Date | Scheduled next follow-up |
| Serial Number | Auto | Generated when status = "Price Offered" |

## Serial Number Format

Serial numbers are automatically generated in the format:
```
XBL/<Project Category>/<Customer Name>/<Date>/<Initial Offer Number>/<Revision>
```

**Example:** `XBL/EPC/ABC Corporation/20260115/1/R1`

## Statuses

- **Connected**: Initial contact established
- **Technical Analysis**: Technical evaluation in progress
- **Price Offered**: Quotation submitted to customer
- **Won**: Deal closed successfully
- **Completed**: Project completed
- **Lost**: Deal lost

## Priority Levels

- **P-1**: Highest priority
- **P-2**: High priority
- **P-3**: Medium priority
- **P-4**: Low priority

## Future Enhancements

- User authentication and role-based access
- Email notifications for follow-ups
- Document attachment for leads
- Advanced reporting and analytics
- CRM integrations
- Mobile app version
- Data export functionality

## Support

For issues or questions, please contact your administrator.

---

**Version:** 1.0
**Last Updated:** January 2026