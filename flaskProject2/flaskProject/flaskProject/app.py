from flask import Flask, request, render_template, session, redirect, url_for, abort
import sqlite3
app = Flask(__name__)

app.secret_key = "Bach"
@app.route('/')
def index():
    if 'username' in session :
        current_username = session['current_user']['name']
    else :
        current_username = ""
    return render_template('SearchWithCSSDataDBAddToCartTable.html', search_text="",
                           user_name = current_username)

@app.route('/login', methods=['GET','POST'])
def login():
    # Khi nhận dữ liệu từ hành vi POST, sau khi nhận dữ liệu
    # từ session sẽ gọi định tuyến sang trang index
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Store 'username' in the session
        obj_user = get_obj_user(username, password)
        if int(obj_user[0]) > 0 : #  Nếu tồn tại ID
            obj_user = {
                "id": obj_user[0],
                "name": obj_user[1],
                "email": obj_user[2]
            }
        if check_exists(username, password):
            session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/searchData', methods=['POST'])
def searchData():
    if 'current_user' in session :
        current_username = session['username']['name']
    else :
        current_username = ""
    search_text = request.form['searchInput']
    product_table = load_data_from_db(search_text)
    print(product_table)
    return render_template('SearchWithCSSDataDBAddToCartTable.html', search_text=search_text,
                           products=product_table, user_name = current_username)

def get_obj_user(username, password) :
    result = []
    sqldbname = 'db/website.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()

    sqlcommand = "SELECT * FROM user WHERE name=? and password=?"
    cursor.execute(sqlcommand, (username, password))
    obj_user = cursor.fetchone()
    conn.close()
    if obj_user:
        result = obj_user
        return result
    else:
        abort(400, "User not found")

def  check_exists(username, password):
    result = False;
    sqldbname = 'db/website.db'
    # Khai báo biến tro toi db
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()

    #sqlcommand = "Select * from storages where"
    sqlcommand = "Select * from user where name ='"+username+"' and password = '"+password+"'"
    cursor.execute(sqlcommand)
    data = cursor.fetchall()
    print(type(data))
    if len(data)>0:
        result=True
    conn.close()
    return result;
def load_data_from_db(search_text):
    sqldbname = 'db/website.db'
    if search_text != "":
        conn = sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        sqlcommand = "select * from storages where model like '%" + search_text+"%'"
        cursor.execute(sqlcommand)
        data = cursor.fetchall()
        conn.close()
        return data

@app.route('/cart/add', methods=["POST"])
def add_to_cart():
    sqldbname = 'db/website.db'
    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])
    connection = sqlite3.connect(sqldbname)
    cursor = connection.cursor()
    cursor.execute("SELECT model, price, picture, details " +
                   "FROM storages WHERE id = ?",
                   (product_id,))
    product = cursor.fetchone()
    connection.close()
    product_dict = {
        "id": product_id,
        "name": product[0],
        "price": product[1],
        "quantity": quantity,
        "picture": product[2],
        "details": product[3]
    }
    cart = session.get("cart", [])
    found = False
    for item in cart :
        if item["id"] == product_id:
            item["quantity"] += quantity
            found = True
            break
    if not found :
    #6.2 add the new product to the cart
        cart.append(product_dict)
    #7. Save the cart back to the session
    session["cart"] = cart

    #8. print out
    rows = len(cart)
    print(rows)
    outputmessage = ("Product added to cart successfully !"
                     f"</br>Current: "+str(rows) + "products"
                     f'<br>Continue Search ! <a href="/">Search Page>/a>'
                     f'</br>View Shopping Cart! <a href="/view_cart">View Cart</a>')
    return outputmessage

@app.route('/update_cart', methods=['POST'])
def update_cart() :
    cart = session.get('cart', [])
    new_cart = []
    for product in cart :
        product_id = str(product['id'])
        if f'quantity-{product_id}' in request.form :
            quantity = int(request.form[f'quantity-{product_id}'])
            if quantity == 0 or f'delete-{product_id}' in request.form :
                continue
        product['quantity'] = quantity
        new_cart.append(product)
        session['cart'] = new_cart
        return redirect(url_for('view_cart'))

@app.route('/proceed_cart', methods=['POST'])
def proceed_cart() :
    if 'current_user' in session :
        user_id = session['current_user']['id']
        user_email = session['current_user']['email']
    else :
        user_id = 0
    if 'cart' in session :
        shopping_cart = session.get("cart", [])
    # 3: Save order information to the "order" table
    #estalblish a database connection
    sqldbname = 'db/website.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    user_address = "User Address"
    user_mobile = "User Mobile"
    purchase_date = "2030-10-10"
    ship_date = "2030-10-15"
    status = 1
    cursor.execute('''INSERT INTO "order" (user_id, user_email, user_address, user_mobile, purchase_date,
    ship_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, user_email, user_address, user_mobile,
                                                         purchase_date, ship_date, status))
    # 4: Get the ID of the inserted order
    order_id = cursor.lastrowid
    print(order_id)
    conn.commit()
    conn.close()
    # 5: Save Order Detail to the "order_details" Table
    # Establish a new database connection (or reuse the existing connection)
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    # Insert order details into the "order_details" table
    for product in shopping_cart :
        product_id = product['id']
        price = product['price']
        quantity = product['quantity']
        cursor.execute('''INSERT INTO order_details (order_id, product_id, price, quantity) VALUES (?, ?, ?, ?)''',
                       (order_id,product_id, price, quantity))
    # 6: Commit the changes and close the connection
    conn.commit()
    conn.close()
    if 'cart' in session :
        current_cart = session.pop("cart", [])
    else :
        print("No current_cart in session.")
    order_url = url_for('orders', order_id=order_id, _external=True)
    return f'Redirecting to order page: <a href="{order_url}"> {order_url}</a>'

@app.route('/orders/', defaults={'order_id': None}, methods=['GET'])
@app.route('/orders/<int:order_id>/', methods=['GET'])
def orders(order_id) :
    sqldbname = 'db/website.db'
    # if 'current_user' in session :
    # user_id = session['current_user']['id']
    user_id = session.get('current_user', {}).get('id')
    if user_id :
        conn = sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        if order_id is not None :
            cursor.execute('SELECT * FROM "order" WHERE id = ? AND user_id = ?', (order_id, user_id))
            order = cursor.fetchone()
            cursor.execute('SELECT * FROM  "order_details" WHERE order_id = ?', (order_id))
            order_details = cursor.fetchall()
            conn.close()
            return render_template('order_details.html', order=order, order_details=order_details)
        else :
            cursor.execute('SELECT * FROM "order" WHERE user_id = ?', (user_id))
            user_orders = cursor.fetchall()
            conn.close()
            return render_template('orders.html', orders=user_orders)
    return "User not logged in."

@app.route("/viewcart", methods=['GET'])
def view_cart() :
    current_cart = []
    if 'cart' in session :
        current_cart = session.get("cart", [])
    if 'current_user' in session :
        current_username = session['current_user']['name']
    else :
        current_username = ""
    return render_template("cart_update.html",
                           carts = current_cart, user_name = current_username)

if __name__ == '__main__':
    app.run(debug=True)