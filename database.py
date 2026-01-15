import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "crm_database.db"


def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)


def init_database():
    """Initialize database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Project Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES project_categories(id)
        )
    ''')

    # Create Leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            project_category TEXT NOT NULL,
            assigned_sales_person TEXT NOT NULL,
            offer_created DATE NOT NULL,
            lead_through TEXT NOT NULL,
            scope_of_work TEXT,
            status TEXT NOT NULL DEFAULT 'Connected',
            initial_offer_number INTEGER NOT NULL,
            offer_revision_number TEXT NOT NULL,
            offered_value REAL,
            priority TEXT NOT NULL DEFAULT 'P-2',
            follow_up_by TEXT,
            follow_up_status TEXT,
            follow_up_date DATE,
            next_follow_up_date DATE,
            serial_number TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')

    conn.commit()
    conn.close()


# Employee Functions
def add_employee(name, email="", phone=""):
    """Add a new employee"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO employees (name, email, phone) VALUES (?, ?, ?)',
            (name, email, phone)
        )
        conn.commit()
        conn.close()
        return True, "Employee added successfully"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Employee already exists"
    except Exception as e:
        conn.close()
        return False, str(e)


def get_all_employees():
    """Get all employees"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM employees ORDER BY name')
    employees = [row[0] for row in cursor.fetchall()]
    conn.close()
    return employees


def delete_employee(name):
    """Delete an employee"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE name = ?', (name,))
    conn.commit()
    conn.close()


# Customer Functions
def add_customer(name, contact_person="", email="", phone="", address=""):
    """Add a new customer"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO customers (name, contact_person, email, phone, address) VALUES (?, ?, ?, ?, ?)',
            (name, contact_person, email, phone, address)
        )
        conn.commit()
        conn.close()
        return True, "Customer added successfully"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Customer already exists"
    except Exception as e:
        conn.close()
        return False, str(e)


def get_all_customers():
    """Get all customers"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM customers ORDER BY name')
    customers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return customers


def get_customer_id(customer_name):
    """Get customer ID by name"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM customers WHERE name = ?', (customer_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def update_customer(name, contact_person="", email="", phone="", address=""):
    """Update customer information"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE customers SET contact_person = ?, email = ?, phone = ?, address = ? WHERE name = ?',
            (contact_person, email, phone, address, name)
        )
        conn.commit()
        conn.close()
        return True, "Customer updated successfully"
    except Exception as e:
        conn.close()
        return False, str(e)


def get_customer_details(customer_name):
    """Get customer details"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT contact_person, email, phone, address FROM customers WHERE name = ?',
        (customer_name,)
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"contact_person": result[0], "email": result[1], "phone": result[2], "address": result[3]}
    return None


# Project Category Functions
def add_project_category(category):
    """Add a new project category"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO project_categories (category) VALUES (?)', (category,))
        conn.commit()
        conn.close()
        return True, "Project category added successfully"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Category already exists"
    except Exception as e:
        conn.close()
        return False, str(e)


def get_all_project_categories():
    """Get all project categories"""
    return ["EPC", "ISS", "PSE", "SPP"]


# Lead Functions
def get_next_initial_offer_number(customer_name, project_category):
    """Get next initial offer number for a customer and project category"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT MAX(initial_offer_number) FROM leads 
           WHERE customer_id = (SELECT id FROM customers WHERE name = ?) 
           AND project_category = ?''',
        (customer_name, project_category)
    )
    result = cursor.fetchone()
    conn.close()
    max_num = result[0] if result[0] else 0
    return max_num + 1


def get_next_offer_revision_number(customer_name, project_category, initial_offer_number):
    """Get next offer revision number"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT MAX(CAST(SUBSTR(offer_revision_number, 2) AS INTEGER)) FROM leads 
           WHERE customer_id = (SELECT id FROM customers WHERE name = ?) 
           AND project_category = ? 
           AND initial_offer_number = ?''',
        (customer_name, project_category, initial_offer_number)
    )
    result = cursor.fetchone()
    conn.close()
    max_num = result[0] if result[0] else 0
    return f"R{max_num + 1}"


def generate_serial_number(project_category, customer_name, offer_created_date, initial_offer_number, offer_revision_number):
    """Generate serial number: XBL/<Project Category>/<Customer Name>/<date>/<Initial Offer number>/<Offer Revision Number>"""
    date_str = offer_created_date.strftime("%Y%m%d")
    serial = f"XBL/{project_category}/{customer_name}/{date_str}/{initial_offer_number}/{offer_revision_number}"
    return serial


def add_lead(customer_id, project_category, assigned_sales_person, offer_created, lead_through,
             scope_of_work, status, initial_offer_number, offer_revision_number, offered_value,
             priority, follow_up_by, follow_up_status, follow_up_date, next_follow_up_date, serial_number=None):
    """Add a new lead"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get customer name for serial number generation
    cursor.execute('SELECT name FROM customers WHERE id = ?', (customer_id,))
    customer_result = cursor.fetchone()
    customer_name = customer_result[0] if customer_result else ""
    
    # Generate serial number if status is "Price Offered"
    if status == "Price Offered" and not serial_number:
        serial_number = generate_serial_number(
            project_category, customer_name, offer_created, 
            initial_offer_number, offer_revision_number
        )
    
    try:
        cursor.execute(
            '''INSERT INTO leads (customer_id, project_category, assigned_sales_person, offer_created,
                                 lead_through, scope_of_work, status, initial_offer_number, 
                                 offer_revision_number, offered_value, priority, follow_up_by,
                                 follow_up_status, follow_up_date, next_follow_up_date, serial_number)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (customer_id, project_category, assigned_sales_person, offer_created,
             lead_through, scope_of_work, status, initial_offer_number,
             offer_revision_number, offered_value, priority, follow_up_by,
             follow_up_status, follow_up_date, next_follow_up_date, serial_number)
        )
        conn.commit()
        conn.close()
        return True, "Lead added successfully"
    except Exception as e:
        conn.close()
        return False, str(e)


def get_all_leads():
    """Get all leads"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT l.id, c.name, l.project_category, l.assigned_sales_person, 
                  l.offer_created, l.status, l.initial_offer_number, l.offer_revision_number,
                  l.priority, l.follow_up_date, l.next_follow_up_date, l.serial_number
           FROM leads l
           JOIN customers c ON l.customer_id = c.id
           ORDER BY l.created_at DESC'''
    )
    leads = cursor.fetchall()
    conn.close()
    return leads


def get_lead_by_id(lead_id):
    """Get lead details by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT l.*, c.name as customer_name FROM leads l
           JOIN customers c ON l.customer_id = c.id
           WHERE l.id = ?''',
        (lead_id,)
    )
    lead = cursor.fetchone()
    conn.close()
    return lead


def update_lead(lead_id, **kwargs):
    """Update lead information"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Build update query dynamically
    update_fields = []
    values = []
    for key, value in kwargs.items():
        update_fields.append(f"{key} = ?")
        values.append(value)
    
    values.append(lead_id)
    
    if update_fields:
        query = f"UPDATE leads SET updated_at = CURRENT_TIMESTAMP, {', '.join(update_fields)} WHERE id = ?"
        try:
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            return True, "Lead updated successfully"
        except Exception as e:
            conn.close()
            return False, str(e)
    
    conn.close()
    return False, "No fields to update"


def get_leads_by_status(status):
    """Get leads by status"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT l.id, c.name, l.project_category, l.assigned_sales_person,
                  l.offer_created, l.status, l.initial_offer_number, l.offer_revision_number,
                  l.priority, l.follow_up_date, l.next_follow_up_date, l.serial_number
           FROM leads l
           JOIN customers c ON l.customer_id = c.id
           WHERE l.status = ?
           ORDER BY l.created_at DESC''',
        (status,)
    )
    leads = cursor.fetchall()
    conn.close()
    return leads


def get_leads_needing_followup(today_date):
    """Get leads that need follow-up today or earlier"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT l.id, c.name, l.project_category, l.assigned_sales_person,
                  l.offer_created, l.status, l.follow_up_date, l.next_follow_up_date
           FROM leads l
           JOIN customers c ON l.customer_id = c.id
           WHERE l.next_follow_up_date IS NOT NULL 
           AND l.next_follow_up_date <= ?
           AND l.status NOT IN ('Won', 'Lost', 'Completed')
           ORDER BY l.next_follow_up_date ASC''',
        (today_date,)
    )
    leads = cursor.fetchall()
    conn.close()
    return leads
