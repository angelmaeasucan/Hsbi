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
                    'id': len(sales) + 1,
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

    template = 'cashier/Sales.html' if session.get('role') == 'cashier' else 'admin/Sales.html'

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