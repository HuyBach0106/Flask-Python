from flask import Flask, request, jsonify, requests, render_template, flash, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'Bach'
base_url =  'http://127.0.0.1:5000/users'
sqldbname = 'db/website.db'

@app.route('/')
def index():  # put application's code here
    # Get all users from the web api
    response = requests.get(base_url)
    # Check if the response is successful
    if response.status_code == 200 :
        # Parse the response as a JSON object
        users = response.json()
        return render_template('user.html', users=users)
    else :
        flash('Something went wrong. Please try again later.')
        return render_template('user.html')

@app.route('/users', methods=['GET'])
def get_users() :
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute('SELECT * FROM user')
    users = cur.fetchall()
    users_list = []
    for user in users :
        users_list.append({'id': user[0], 'name': user[1], 'email': user[2],
                           'password': user[3]})
    return jsonify(users_list)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id) :
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute('SELECT * FROM user WHERE id = ?', (id,))
    user = cur.fetchone()
    if user :
        user_dict = {'id': user[0], 'name': user[1],
                     'email': user[2], 'password': user[3]}
        return jsonify(user_dict)
    else :
        return 'User not found', 404

@app.route('/users', methods=['POST'])
def add_user() :
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    user_name = request.json.get('name')
    user_email = request.json.get('email')
    user_password = request.json.get('password')
    if user_name and user_email and user_password :
        cur.execute('INSERT INTO user(name, email, password) '
                    'VALUES (?,?,?)', (user_name, user_email, user_password))
        conn.commit()
        user_id = cur.lastrowid
        return jsonify({'id': user_id})
    else :
        return 'User name, email and password are required', 400

@app.route('/add', methods=['GET', 'POST'])
def add() :
    if request.method == 'POST' :
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        if user_name and user_email and user_password :
            response = requests.post(base_url)
            json={'name': user_name, 'email': user_email, 'password': user_password}
            if response.status_code == 200 :
                user = response.json()
                flash(f'User {user["id"]} added sucessfully.')
                return redirect('/')
            else :
                flash('Something went wrong. Please try again later.')
                return render_template('users/add.html')
        else :
            flash('User name, email and password are required')
            return render_template('add.html')
    else :
        return render_template('users/add.html')

@app.route('/users/<int:id>', methods =['PUT'])
def update_user(id) :
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    user_name = request.json.get('name')
    user_email = request.json.get('email')
    user_password = request.json.get('password')
    if user_name and user_email and user_password :
        cur.execute('UPDATE user SET name = ?, email = ?' 
                    'password = ? WHERE id = ?', (user_name, user_email, user_password, id))
        conn.commit()
        if cur.rowcount > 0 :
            return jsonify({'message': 'User updated successfully'})
        else :
            return 'User name, email and password are required', 400

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id) :
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        if user_name and user_email and user_password:
            response = requests.put(f'{base_url}/{id}',
            json = {'name': user_name, 'email': user_email, 'password': user_password})
            if response.status_code == 200 :
                flash(f'User {id} updated successfully')
                return redirect('/')
            else :
                flash('Something went wrong, please try again later.')
                return render_template('edit.html')
        else :
            flash('User name, email and password are required.')
    else :
        response = requests.get(f'{base_url}/{id}')
    if response.status_code == 200 :
        user = response.json()
        return render_template('edit.html', user=user)
    else :
        flash('User Not Found.')
        return render_template('edit.html')


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id) :
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute('DELETE FROM user WHERE id = ?', (id,))
    conn.commit()
    if cur.rowcount > 0 :
        return jsonify({'message': 'User deleted successfully'})
    else :
        return 'User not found', 404

@app.route('/users/<int:id>', methods=['DELETE'])
def delete(id) :
    if request.method == 'POST' :
        response = requests.delete(f'{base_url}/{id}')
        if response.status_code == 200 :
            flash(f'User {id} deleted sucessfully.')
            return redirect('/')
        else :
            flash('Something went wrong. Please try again later.')
            return render_template('delete.html')
    else :
        response = requests.get(f'{base_url}/{id}')
    if response.status_code == 200 :
        user = response.json()
        return render_template('delete.html', user=user)
    else :
        flash('User Not Found.')
        return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
