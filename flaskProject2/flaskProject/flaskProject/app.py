from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
app = Flask(__name__)

app.secret_key = "Bach"
@app.route('/')
def index():
    return render_template('SearchWithCSSDataDB.html', search_text="")


@app.route('/searchData', methods=['POST'])
def searchData():
    search_text = request.form['searchInput']
    html_table = load_data_from_db(search_text)
    print(html_table)
    return render_template('SearchWithCSSDataDBAddToCartTable.html', search_text=search_text, carts = html_table)

@app.route('/login', methods=['GET','POST'])
def login():
    print('1');
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_exists(username, password):
            session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')
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
    quantity = request.form["quantity"]
    connection = sqlite3.connect(sqldbname)
    cursor = connection.cursor()
    cursor.execute("SELECT model, price " +
                   "FROM storages WHERE id = ?",
                   (product_id,))
    product = cursor.fetchone()
    connection.close()
    product_dict = {
        "id": product_id,
        "name": product[0],
        "price": product[1],
        "quantity": quantity
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
                     "<br>Current: "+str(rows) + " products")
    return outputmessage

@app.route("/cart")
def view_cart() :
    current_cart = []
    if 'cart' in session :
        current_cart = session.get("cart", [])
    return render_template("cart.html",
                           carts = current_cart)

if __name__ == '__main__':
    app.run()