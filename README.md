# Members
## • Angel Mae B. Asucan
## • Jhonavie B. Dico
## • Bea Rose A. Pacaldo
## • Isagani Dacapio
# BSCS - 1A

# Username: admin
# Password: admin

# Username: cashier
# Password: cashier

# Title and Description: HomeTech Solution
## • The HomeTech Solution is a menu driven application that generate invoices, records monthly payment and monitor outstanding balances. It is design for customer who purchased products such as motorcycle, refrigerators, television, washing machine and other products an installment basis. The system helps staff accurately track customer payments, compute remaining balance and produce billing and payment records.

# Prerequisites
## • Python (version 3.x)
## • Flask
## • Web browser (Google Chrome, Edge, etc.)
## • Code editor (VS code recommended)

# Installation
## Follow these steps to run the projects:
## Clone the repository
## • git clone https://github.com/angelmaeasucan/hometech-solution.git

## Go to project folder
## • cd hometech-solution

## Install Flask (if not installed)
## • pip install flask

## Run the application
## • python.py

## Then open your browser and go to:
## • http://127.0.0.1:5000/

# Usage
## • Open the system in your browser
## • Log in using your username and password
## • Access the dashboard
## • Add or manage customer information
## • Create billing transactions (cash or installment)

## Example (Python Flask Route)
## • @app.route('/dashboard')
##   def dashboard():
##        return render_template('dashboard.html')

# Module 1
# Customer Management Module
## • The Customer Management Module is a core component of the system designed to facilitate the organization, storage, retrieval, and maintenance of customer data. Built as a web-based application (indicated by the development context referencing Flask framework), this module enables users to perform key operations such as adding new customer records and searching for existing entries. It is developed with a user-centric interface and structured data handling to ensure ease of use and data accuracy.
 
# Key Features & Functionalities
 
# Add New Customer
### • Data Entry Form: A structured input section that captures essential customer details:
### • Customer ID: Unique identifier assigned to each customer to ensure record distinctiveness.
### • Customer Name: Full name of the customer.
### • Contact No.: Valid phone or mobile number for communication purposes.
### • Address: Physical location of the customer.

## Operation Buttons:
### • Save Button: A green-colored interactive button that submits and stores the entered information into the system database after basic validation.
### • Clear Button: A red-colored interactive button that resets all input fields to empty, allowing users to restart data entry without navigating away.
 
# Search and Retrieve Customer
## Search Functionality:
​• A dedicated search bar labeled "Search by ID or Name", which accepts partial or full inputs of Customer ID or Customer Name.
​• Search Button: Green-colored button that triggers the system to filter and display records matching the entered criteria.
​• Show All Button: Blue-colored button that retrieves and displays all stored customer records at once, bypassing filtering.
​
# Result Display:
​• A structured table titled "All Customers" that lists retrieved data with columns: Customer ID, Name, Contact, Address, and Actions.
​​• The table also displays the total count of available records (e.g., "All Customers (7)"), providing users with immediate visibility on data volume.

# Record Management
### • Delete Function: Under the Actions column, each customer record is paired with a red-colored Delete button. This enables authorized users to remove obsolete or incorrect records from the system.


# Module 2: Appliances Product Management

# Description
## This module is used to manage appliance products in a system. It helps the user add, update, view, and delete product information in an organized way. It also makes sure that each product has correct details before being saved.

## Features
### • Add new appliances
### • Update product details
### • View available products
### • Delete products
### • Validates product information (unique ID, correct price, valid stock)

## How it works
### • User inputs product details (Product ID, Product name, price, select status)
### • User can search customers
### • System checks if Product ID is unique
### • System verifies that price is greater than 0
### • System ensures stock quantity is not negative
### • If all conditions are met, the product is saved
### • User can then view, update, or delete the product anytime

# Module 3: Sales and Installment Processing
## Description
### • A system module for handling sales and installment transactions
### • Allows users to process purchases using cash or installment payments
### • Manages product selection, payments, and automatic computation of monthly dues

# Features / Functionalities
### • Create new sales transaction
### • Start and record a new sale
### • Select appliances to buy
### • Choose one or more items from available stock
### • Choose payment type (Cash / Installment)
### • Decide whether the payment is full or partial over time
### • Record down payment
### • Input the initial payment amount
### • Set installment term (e.g., 12 months)
### • Define how long the payment will be divided
### • Automatic monthly amortization calculation
### • System computes the monthly payment amount
### • Inventory is updated once the sale is confirmed

## Rules
### • At least one appliance must be selected
### • A payment type must be chosen
### • Down payment must not exceed the total price
### • For installment, monthly payment must be generated
### • Cannot proceed if the item is out of stock

# How It Works
## Step 1: Create transaction
### • User starts a new sale
## Step 2: Enter appliances want to buy
### • Choose items from inventory
### • System checks stock availability
## Step 3: Choose payment type
### • Cash → full payment
### • Installment → proceed to next steps
## Step 4: Enter payment details (if installment)
### • Input down payment
### • Set installment term (e.g., 12 months)
### • System calculates monthly amortization
## Step 5: Validation
### • Ensure all rules are followed (item selected, valid payment, stock available)
## Step 6: Approval
### • Transaction is approved if all conditions are met

Module 4: Billing and Invoice Management
Description

This module handles the creation, tracking, and management of billing and invoices. It ensures that payments are properly recorded, balances are updated, and invoices are generated accurately. It also helps monitor due dates and payment status for better financial tracking.

Functionalities 
Generate official invoice
Display breakdown (total price, down payment, balance)
Update remaining balance after payment
Monitor due dates
Track invoice status (paid / ongoing / overdue)
Print invoice and payment receipt

Rules 
Invoice number must be unique
All computations must be automatic
Balance must auto-update
Due date must follow installment schedule
Status updates automatically
Only authorized staff can modify invoice

How It Works 
System generates an invoice when a transaction is made
It computes the total price automatically
Shows breakdown:
Total price
Down payment
Remaining balance

When payment is made:
System updates the remaining balance
System tracks due dates based on installment schedule
Invoice status is updated:
  Partial
  Paid
  Pending
User can print invoice and receipt
Only authorized staff can edit or modify invoice details

Module 5: Payment Monitoring and Collection
Description

This module focuses on tracking customer payments and managing overdue accounts.It helps ensure that all payments are monitored and unpaid balances are identified.

Functionalities
View payment history per customer
Identify overdue accounts
Generate overdue reminder list

Rules
Payment amount must be positive
Payment records cannot be deleted
Accounts are marked overdue if unpaid after due date
Only unpaid invoices appear in the overdue list

Roles Involved
Admin
Can view all payment records
Can monitor overdue accounts
Cashier/Staff
Can view payment history
Can assist in tracking unpaid customers

How It Works
The system records every payment made by customers.
It automatically checks due dates and flags unpaid accounts as overdue.
When needed, the system generates a list of customers with unpaid balances.
Users (admin or cashier) can review payment history and follow up on overdue accounts.

Module 6: Report and Management Overview
Description
This module provides summarized reports for business monitoring and decision-making. It organizes sales and payment data into useful reports.

Functionalities
Daily sales report
Monthly installment collection report
Outstanding balance report
Best-selling appliances report

Rules
Reports are based on completed transactions
Reports use recorded payments only
Only unpaid balances are shown in outstanding reports
Sales reports are based on sales data

Roles Involved
Admin
Main user of reports
Uses reports for analysis and decision-making
Cashier/Staff
May view reports (depending on access)
Helps ensure accurate data entry for reports

How It Works
The system collects data from sales and payment records.
It automatically generates reports based on selected timeframes (daily/monthly).
Only valid and completed transactions are included.
Admin can review reports to track performance, balances, and top products.

Module 7: User Roles and Security
Description

This module controls system access and defines what each user can or cannot do. It ensures security and proper role management.

Functionalities
Manage users
Monitor payments
Process sales
Record payments
Print invoices

Roles
Admin
Full access to all functionalities
Can manage users and system settings
Cashier/Staff
Limited access
Focus on sales, payments, and invoices only

How It Works
The system assigns roles (Admin or Cashier/Staff) to each user.
Each role has specific permissions:
Admin can access everything, including user management.
Cashier cannot access restricted pages (like user management).
When a user logs in, the system checks their role.
Based on their role, only allowed pages and features are shown.
