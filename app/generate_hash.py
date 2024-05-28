from werkzeug.security import generate_password_hash

# Genera el hash para la contraseña 'adminpassword'
hashed_password = generate_password_hash('adminpassword', method='pbkdf2:sha256')
print(hashed_password)
