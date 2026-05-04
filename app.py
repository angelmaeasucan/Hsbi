from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Add a secret key for sessions

# --- DATABASES ---
customers = [
    {'id': '0101', 'name': 'Juan', 'contact': '09223456789', 'address': 'Tubigon'},
    {'id': '0000', 'name': 'Jhonavie', 'contact': '09220987654', 'address': 'Clarin'},
    {'id': '0001', 'name': 'Angel', 'contact': '09123456789', 'address': 'Dagohoy'},
    {'id': '0002', 'name': 'Maria', 'contact': '09123452459', 'address': 'Danao'},
    {'id': '0003', 'name': 'John', 'contact': '09123456789', 'address': 'Mactan'},
    {'id': '0004', 'name': 'Jane', 'contact': '09123456789', 'address': 'Bantayan'},
    {'id': '0005', 'name': 'Heart', 'contact': '09958840258', 'address': 'Nahud'},
]

products = [
    {'id': '1001', 'name': 'Laptop', 'category': 'Electronics', 'price': 45000, 'stock': 'Available', 'status': 'active'},
    {'id': '1010', 'name': 'Television', 'category': 'Electronics', 'price': 32000, 'stock': 'Available', 'status': 'active'},
    {'id': '1234', 'name': 'Refrigerator', 'category': 'Appliances', 'price': 23000, 'stock': 'Available', 'status': 'active'},
    {'id': '1235', 'name': 'Washing Machine', 'category': 'Appliances', 'price': 18000, 'stock': 'Available', 'status': 'active'},
    {'id': '14000', 'name': 'Printer', 'category': 'Electronics', 'price': 5000, 'stock': 'Not Available', 'status': 'active'},
    {'id': '1237', 'name': 'Blender', 'category': 'Appliances', 'price': 2000, 'stock': 'Available', 'status': 'active'},
    {'id': '1238', 'name': 'Toaster', 'category': 'Appliances', 'price': 1500, 'stock': 'Available', 'status': 'active'},
]

sales = [
     {'id': '0000', 'product': 'Television', 'quantity': 1, 'total': 32000, 'date': '2024-06-01', 'customer': 'Jhonavie', 'payment_type': 'cash'},
     
]

bills = [
    {'id': 1, 'customer_id': '0000', 'customer': 'Jhonavie', 'amount': 32000, 'date': '2024-06-01', 'status': 'Paid', 'description': 'Television purchase', 'type': 'Full Payment'},
]

activities = []

user_credentials = {
    'admin': {'password': 'admin', 'role': 'admin'},
    'cashier': {'password': 'cashier', 'role': 'cashier'}
}

# --- HELPER FUNCTIONS ---
def log_activity(activity_type, description, user="System"):
    global activities
    activity = {
        'id': len(activities) + 1,
        'type': activity_type,
        'description': description,
        'user': user,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    activities.insert(0, activity)
    if len(activities) > 20:
        activities = activities[:20]

def get_dashboard_metrics():
    total_customers = len(customers)
    total_sales = sum(s['total'] for s in sales)
    total_products = len(products)
    total_products_sold = sum(s['quantity'] for s in sales)
    pending_payments = sum(b['amount'] for b in bills if b['status'] == 'Unpaid')
    total_bills = len(bills)
    paid_bills = len([b for b in bills if b['status'] == 'Paid'])
    unpaid_bills = len([b for b in bills if b['status'] == 'Unpaid'])
    pending_bills = len([b for b in bills if b['status'] == 'Pending'])
    total_revenue = sum(b['amount'] for b in bills if b['status'] == 'Paid')
    return {
        'total_customers': total_customers,
        'total_sales': total_sales,
        'total_products': total_products,
        'total_products_sold': total_products_sold,
        'pending_payments': pending_payments,
        'total_bills': total_bills,
        'paid_bills': paid_bills,
        'unpaid_bills': unpaid_bills,
        'pending_bills': pending_bills,
        'total_revenue': total_revenue,
        'billing_data': bills,
        'activity_log': activities,
        'recent_activities': activities[:10],
        'recent_bills': bills[-5:]
    }

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()

        if username in user_credentials:
            if password == user_credentials[username]['password']:
                log_activity('login', f'User {username} logged in', username)
                role = user_credentials[username]['role']
                session['username'] = username
                session['role'] = role
                if role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif role == 'cashier':
                    return redirect(url_for('cashier_dashboard'))
            else:
                error = "Invalid username or password!"
        else:
            error = "Invalid username or password!"
    return render_template('login.html', error=error)

@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html', **get_dashboard_metrics())

@app.route('/cashier')
def cashier_dashboard():
    return render_template('cashier/dashboard.html', **get_dashboard_metrics())

@app.route('/customer_management', methods=['POST', 'GET'])
def customer_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session.get('role') == 'cashier' and request.method == 'POST':
        return redirect(url_for('customer_management'))
    global customers
    error = None
    search_query = ''
    if request.method == 'POST':
        if 'save_customer' in request.form:
            c_id = request.form.get('customerId', '').strip()
            c_name = request.form.get('customerName', '').strip()
            contact = request.form.get('contactNo', '').strip()
            address = request.form.get('address', '').strip()
            if not c_id or not c_name or not contact:
                error = "Customer ID, Name, and Contact are required!"
            else:
                if any(c['id'] == c_id for c in customers):
                    error = "Customer ID already exists!"
                else:
                    customers.append({'id': c_id, 'name': c_name, 'contact': contact, 'address': address, 'status': 'Active'})
                    log_activity('customer', f'Added: {c_name}', 'admin')
                    return redirect(url_for('customer_management'))
        elif 'search_customer' in request.form:
            search_query = request.form.get('searchInput', '').strip().lower()
    
    filtered = [c for c in customers if search_query in c['id'].lower() or search_query in c['name'].lower()] if search_query else customers
    template = 'cashier/customer.html' if session.get('role') == 'cashier' else 'admin/customer.html'
    return render_template(template, customers=filtered, error=error, search_query=search_query)

@app.route('/delete_customer/<customer_id>')
def delete_customer(customer_id):
    global customers
    customers[:] = [c for c in customers if c['id'] != customer_id]
    log_activity('customer', f'Deleted ID: {customer_id}', 'admin')
    return redirect(url_for('customer_management'))

@app.route('/products', methods=['POST', 'GET'])
def products_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session.get('role') == 'cashier' and request.method == 'POST':
        return redirect(url_for('products_management'))
    global products
    error = None
    search_query = ''
    if request.method == 'POST':
        if 'save_product' in request.form:
            p_id = request.form.get('productId', '').strip()
            p_name = request.form.get('productName', '').strip()
            cat = request.form.get('category', '').strip()
            prc = request.form.get('price', '').strip()
            stk = request.form.get('stock', '').strip()
            if not p_id or not p_name or not cat or not prc or not stk:
                error = "All fields are required!"
            else:
                try:
                    if any(str(p['id']) == str(p_id) for p in products):
                        error = "Product ID already exists!"
                    else:
                        products.append({'id': p_id, 'name': p_name, 'category': cat, 'price': float(prc), 'stock': stk, 'status': 'active'})
                        log_activity('product', f'Added: {p_name}', 'admin')
                        return redirect(url_for('products_management'))
                except ValueError: 
                    error = "Invalid Price format!"
        elif 'search_product' in request.form:
            search_query = request.form.get('searchInput', '').strip().lower()
            
    filtered = [p for p in products if search_query in str(p['id']) or search_query in p['name'].lower()] if search_query else products
    template = 'cashier/products.html' if session.get('role') == 'cashier' else 'admin/products.html'
    return render_template(template, products=filtered, error=error, search_query=search_query)

@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    global products
    product = next((p for p in products if str(p['id']) == str(product_id)), None)
    if request.method == 'POST' and product:
        product['name'] = request.form.get('productName')
        product['price'] = float(request.form.get('price'))
        product['category'] = request.form.get('category')
        product['stock'] = request.form.get('stock')
        return redirect(url_for('products_management'))
    return render_template('admin/products.html', products=products, edit_product=product)

@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    global products
    products[:] = [p for p in products if str(p['id']) != str(product_id)]
    return redirect(url_for('products_management'))

@app.route('/sales', methods=['GET', 'POST'])
def sales_management():
    if 'username' not in session:
        return redirect(url_for('login'))

    global sales, bills

    search_query = ''
    filtered = sales  # default display

    if request.method == 'POST':

        # =========================
        # ADD SALE
        # =========================
        if 'add_sale' in request.form:
            prod_name = request.form.get('product')
            cust_name = request.form.get('customer')
            cust_id = request.form.get('customer_id')
            qty = request.form.get('quantity')
            pay_type = request.form.get('payment_type')
            date = request.form.get('date')

            # safe convert quantity
            try:
                qty = int(qty)
            except:
                qty = 0

            matched_prod = next((p for p in products if p['name'] == prod_name), None)

            if matched_prod:
                total_p = matched_prod['price'] * qty

                new_sale = {
                    'id': cust_id,
                    'customer_id': cust_id,
                    'product': prod_name,
                    'customer': cust_name,
                    'customer_id': cust_id,
                    'quantity': qty,
                    'total': total_p,
                    'date': date,
                    'payment_type': pay_type
                }

                sales.append(new_sale)
                        
                if pay_type == 'cash':
                    bills.append({
                        'id': len(bills) + 1,
                        'customer': cust_name,
                        'amount': total_p,
                        'date': date,
                        'status': 'Paid',
                        'description': f'Full payment {prod_name}',
                        'type': 'Full Payment'
                    })

                return redirect(url_for('sales_management'))

        # =========================
        # SEARCH SALE
        # =========================
        elif 'search_sale' in request.form:
            search_query = request.form.get('searchInput', '').strip().lower()

            filtered = []
            for s in sales:
                sale_id = str(s.get('id', '')).lower()
                customer = str(s.get('customer', '')).lower()
                product = str(s.get('product', '')).lower()
                cust_id = str(s.get('customer_id', '')).lower()

                if (
                    search_query in sale_id or
                    search_query in customer or
                    search_query in product or
                    search_query in cust_id
                ):
                    filtered.append(s)

    template = 'cashier/sales.html' if session.get('role') == 'cashier' else 'admin/sales.html'

    return render_template(
        template,
        sales=filtered,
        products=products,
        search_query=search_query
    )
@app.route('/delete_sale/<int:sale_id>', methods=['POST'])
def delete_sale(sale_id):
    global sales
    sales[:] = [s for s in sales if s['id'] != sale_id]
    return redirect(url_for('sales_management'))

@app.route('/billing', methods=['GET', 'POST'])
def billing_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    global bills
    error = None
    if request.method == 'POST':
        if 'add_bill' in request.form:
            customer = request.form.get('customer', '').strip()
            customer_id = request.form.get('customer_id', '').strip()
            amount = request.form.get('amount', '').strip()
            date = request.form.get('date', '').strip()
            status = request.form.get('status', 'Unpaid')
            bill_type = request.form.get('type', 'Manual')
            description = request.form.get('description', '').strip()
            
            if not customer or not amount or not date:
                error = "All fields are required!"
            else:
                try:
                    amount = float(amount)
                    new_id = max([b['id'] for b in bills], default=0) + 1
                    customer_id = ''
                    for c in customers:
                        if c['name'] == customer:
                            customer_id = c['id']
                            break
                    bills.append({
                        'id': new_id,
                        'customer_id': customer_id,
                        'customer': customer,
                        'amount': amount,
                        'date': date,
                        'status': status,
                        'description': description,
                        'type': bill_type
                    })
                    log_activity('billing', f'Bill added for {customer}', session.get('username', 'Unknown'))
                except ValueError:
                    error = "Invalid amount!"
        search_query = request.form.get('searchInput', '').lower()
    else:
        search_query = ''
    
    filtered_bills = [b for b in bills if search_query in b['customer'].lower()] if search_query else bills
    
    metrics = get_dashboard_metrics()
    template = 'cashier/billing.html' if session.get('role') == 'cashier' else 'admin/billing.html'
    return render_template(template, bills=filtered_bills, 
                           total_bills=metrics['total_bills'], paid_bills=metrics['paid_bills'], 
                           unpaid_bills=metrics['unpaid_bills'], total_collected=metrics['total_revenue'],
                           outstanding_amount=sum(b['amount'] for b in bills if b['status'] != 'Paid'),
                           bills_json=json.dumps(filtered_bills), pending_bills=metrics['pending_bills'],
                           search_query=search_query, error=error)

@app.route('/update_bill_status/<int:bill_id>/<status>')
def update_bill_status(bill_id, status):
    for b in bills:
        if b['id'] == bill_id:
            b['status'] = status
    return redirect(url_for('billing_management'))

@app.route('/delete_bill/<int:bill_id>')
def delete_bill(bill_id):
    global bills
    bills = [b for b in bills if b['id'] != bill_id]
    return redirect(url_for('billing_management'))

payments = []


# PAYMENT FORM
@app.route('/payment', methods=['GET', 'POST'])
def payment_form():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        payment_data = {
            "payment_id": request.form.get('payment_id'),
            "payment_date": request.form.get('payment_date'),
            "customer": request.form.get('customer'),
            "customer_id": request.form.get('customer_id'),
            "invoice_no": request.form.get('invoice_no'),
            "due_date": request.form.get('due_date'),
            "payment_type": request.form.get('payment_type'),
            "gcash_number": request.form.get('gcash_number'),
            "reference_number": request.form.get('reference_number'),
            "total_due": request.form.get('total_due'),
            "amount_paid": request.form.get('amount_paid'),
            "remaining_balance": request.form.get('remaining_balance'),
            "payment_status": request.form.get('payment_status'),
            "remarks": request.form.get('remarks'),
            "processed_by": request.form.get('processed_by')
        }

        # SAVE PAYMENT
        payments.append(payment_data)
        log_activity('payment', f"Payment recorded: {payment_data['payment_id']}", session.get('username', 'Unknown'))
        print("\n===== PAYMENT RECORDED =====")
        print(payment_data)

        return redirect(url_for('payment_receipt', payment_id=payment_data['payment_id']))

    template = 'cashier/payment.html' if session.get('role') == 'cashier' else 'admin/payment.html'
    return render_template(
        template,
        customers=customers,
        bills=bills,
        payments=payments,
        now=datetime.now()
    )


@app.route('/payment_receipt/<payment_id>')
def payment_receipt(payment_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    payment = next((p for p in payments if p.get('payment_id') == payment_id), None)
    if payment is None:
        return redirect(url_for('payment_form'))

    return render_template('cashier/payment_receipt.html', payment=payment)


@app.route('/payment_success')
def payment_success():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    last_payment = payments[-1] if payments else None
    template = 'cashier/payment.html' if session.get('role') == 'cashier' else 'admin/payment.html'
    return render_template(template, 
                         success_message="Payment Successfully Recorded!",
                         last_payment=last_payment,
                         customers=customers,
                         bills=bills,
                         payments=payments,
                         now=datetime.now())


# VIEW ALL PAYMENTS
@app.route('/payments')
def view_payments():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('searchInput', '').lower()
    
    filtered_payments = payments
    if search_query:
        filtered_payments = [p for p in payments if search_query in p.get('customer', '').lower() or 
                             search_query in p.get('payment_id', '').lower()]
    
    total_payments = sum(float(p.get('amount_paid', 0)) for p in filtered_payments)
    
    return render_template('cashier/payments.html', 
                         payments=filtered_payments,
                         total_payments=total_payments,
                         search_query=search_query)

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        search_query = request.form.get('searchInput', '').lower()
    else:
        search_query = request.args.get('searchInput', '').lower()

    overdue_bills = [b for b in bills if b['status'] != 'Paid']
    payments_for_report = payments
    if search_query:
        overdue_bills = [b for b in overdue_bills if search_query in b['customer'].lower()]
        payments_for_report = [p for p in payments if search_query in p.get('customer', '').lower() or search_query in p.get('payment_id', '').lower() or search_query in p.get('invoice_no', '').lower()]

    total_overdue = len(overdue_bills)
    overdue_amount = sum(b['amount'] for b in overdue_bills)
    reminder_list = [f"Reminder for {b['customer']}: ₱{b['amount']} due on {b.get('due_date', b['date'])}" for b in overdue_bills]
    template = 'cashier/reports.html' if session.get('role') == 'cashier' else 'admin/reports.html'
    return render_template(template,
                           overdue_bills=overdue_bills,
                           reminder_list=reminder_list,
                           search_query=search_query,
                           total_overdue=total_overdue,
                           overdue_amount=overdue_amount,
                           payments=payments_for_report,
                           total_payments=len(payments_for_report),
                           total_payment_amount=sum(float(p.get('amount_paid', 0)) for p in payments_for_report))

@app.route('/users')
def users():
    user_list = [{'username': k, **v} for k, v in user_credentials.items()]
    return render_template('admin/users.html', users=user_list)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    log_activity('system', 'System Start', 'System')
    app.run(debug=True)
    
def handler(request):
    return app