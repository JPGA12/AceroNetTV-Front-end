from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import load_users, save_users

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'supersecretkey'  # Necesario para usar mensajes flash

# Cargar usuarios desde el archivo JSON
users_db = load_users()

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
            flash(f'Login successful! Welcome {username}', 'success')
            if user['rol'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard', username=username))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['nombre']
        if username in users_db:
            flash('Username already exists', 'danger')
        else:
            new_user = {
                'password': generate_password_hash(request.form['contrasena'], method='pbkdf2:sha256'),
                'cedula': request.form['cedula'],
                'direccion': request.form['direccion'],
                'correo': request.form['correo'],
                'telefono': request.form['telefono'],
                'ciudad': request.form['ciudad'],
                'departamento': request.form['departamento'],
                'ubicacion_geografica': request.form['ubicacion_geografica'],
                'estado': request.form['estado'],
                'fecha_de_corte': request.form['fecha_de_corte'],
                'rol': request.form['rol']
            }
            users_db[username] = new_user
            save_users(users_db)
            flash('User created successfully', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('create_user.html')

@app.route('/read_user', methods=['GET', 'POST'])
def read_user():
    user = None
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_email = request.form['user_email']
        user = next((u for u in users_db.values() if str(u['cedula']) == user_id or u['correo'] == user_email), None)
        if not user:
            flash('User not found', 'danger')
    return render_template('read_user.html', user=user)

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    user = None
    if request.method == 'POST' and 'search' in request.form:
        user_id = request.form['user_id']
        user_email = request.form['user_email']
        user = next((u for u in users_db.values() if str(u['cedula']) == user_id or u['correo'] == user_email), None)
        if not user:
            flash('User not found', 'danger')
    elif request.method == 'POST' and 'update' in request.form:
        user_id = request.form['user_id']
        user = next((u for u in users_db.values() if str(u['cedula']) == user_id), None)
        if user:
            user.update({
                'cedula': request.form['cedula'],
                'direccion': request.form['direccion'],
                'correo': request.form['correo'],
                'telefono': request.form['telefono'],
                'ciudad': request.form['ciudad'],
                'departamento': request.form['departamento'],
                'ubicacion_geografica': request.form['ubicacion_geografica'],
                'estado': request.form['estado'],
                'fecha_de_corte': request.form['fecha_de_corte'],
                'rol': request.form['rol']
            })
            if request.form['contrasena']:
                user['password'] = generate_password_hash(request.form['contrasena'], method='pbkdf2:sha256')
            save_users(users_db)
            flash('User updated successfully', 'success')
        else:
            flash('User not found', 'danger')
    return render_template('update_user.html', user=user)

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_email = request.form['user_email']
        user = next((u for u in users_db.values() if str(u['cedula']) == user_id and u['correo'] == user_email), None)
        if user:
            for username, data in users_db.items():
                if str(data['cedula']) == user_id and data['correo'] == user_email:
                    del users_db[username]
                    break
            save_users(users_db)
            flash('User deleted successfully', 'success')
        else:
            flash('User not found', 'danger')
    return render_template('delete_user.html')

@app.route('/user_dashboard/<username>')
def user_dashboard(username):
    user = users_db.get(username)
    if user:
        return render_template('user_dashboard.html', user=user)
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

@app.route('/user_info/<username>')
def user_info(username):
    user = users_db.get(username)
    if user:
        return render_template('user_info.html', user=user)
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

@app.route('/user_products/<username>')
def user_products(username):
    user = users_db.get(username)
    if user:
        return render_template('user_products.html', user=user)
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

@app.route('/user_invoices/<username>')
def user_invoices(username):
    user = users_db.get(username)
    if user:
        return render_template('user_invoices.html', user=user)
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

@app.route('/user_generate_invoice/<username>')
def user_generate_invoice(username):
    user = users_db.get(username)
    if user:
        return render_template('user_generate_invoice.html', user=user)
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

@app.route('/products')
def products():
    productos = [
        {'nombre': 'Producto 1', 'descripcion': 'Descripción del producto 1'},
        {'nombre': 'Producto 2', 'descripcion': 'Descripción del producto 2'}
    ]
    return render_template('products.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
