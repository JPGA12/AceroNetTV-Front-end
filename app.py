from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar mensajes flash

# Simulación de una base de datos de usuarios en memoria
users_db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_db.get(username)
        if user and check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_db:
            flash('Username already exists', 'danger')
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            users_db[username] = {'password': hashed_password}
            flash('User created successfully', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/products')
def products():
    productos = [
        {'nombre': 'Producto 1', 'descripcion': 'Descripción del producto 1'},
        {'nombre': 'Producto 2', 'descripcion': 'Descripción del producto 2'},
        {'nombre': 'Producto 3', 'descripcion': 'Descripcion del producto 3'}
    ]
    return render_template('products.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
