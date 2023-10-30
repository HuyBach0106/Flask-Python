from flask import Flask, request, render_template, session, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bach'

db_file = 'db/website.db'

def get_db_connection() :
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def index() :
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM storages')
    storages = cursor.fetchall()
    connection.close()
    return render_template('Admin/Storages/index.html', storages=storages)

@app.route('/add', methods=['GET', 'POST'])
def add() :
    if request.method == 'POST':
        product = request.form['product']
        brand = request.form['brand']
        rating = request.form['rating']
        picture = request.form['picture']
        model = request.form['model']
        price = request.form['price']
        RAM = request.form['RAM']
        details = request.form['details']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO storages(product, brand, rating, model, picture, price, RAM,
        details) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ''')
        connection.commit()
        connection.close()
        flash('Storage added successfully', 'success')
        return redirect(url_for('index'))
    return render_template('Admin/storages/add.html')

@app.route('/edit/<int:storage_id>', methods=['GET', 'POST'])
def edit(storage_id) :
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM storages WHERE id = ?', (storage_id,))
    storage = cursor.fetchone()
    connection.close()
    if request.method == 'POST' :
        product = request.form['product']
        brand = request.form['brand']
        rating = request.form['rating']
        picture = request.form['picture']
        model = request.form['model']
        price = request.form['price']
        RAM = request.form['RAM']
        details = request.form['details']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''UPDATE storages SET product=?, brand=?, rating=?, model=?,picture=?, price=?, RAM=?,
        details=? WHERE id=?''', (product, brand, rating, model, picture, price, RAM, details, storage_id))
        connection.commit()
        connection.close()
        flash('Storage updated successfully', 'success')
        return redirect(url_for('index'))

    @app.route('/delete/<int:storage_id>', methods=['POST'])
    def delete(storage_id) :
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM storages WHERE id = ?', (storage_id,))
        connection.commit()
        connection.close()
        flash('Storage deleted successfully', 'success')
        return redirect(url_for('index'))

if __name__ == '__main__' :
    app.run(debug=True)
