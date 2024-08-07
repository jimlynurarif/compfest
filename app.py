from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient('mongo', 27017)
db = client['sea_salon']
users_collection = db['users']
reviews_collection = db['reviews']
reservations_collection = db['reservations']
services_collection = db['services']
branches_collection = db['branches']

@app.route('/')
def index():
    branches = list(branches_collection.find())
    if 'user_id' in session:
        return render_template('index.html', branches=branches)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
    return render_template('auth.html', title='Login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = {
            'full_name': full_name,
            'email': email,
            'phone_number': phone_number,
            'password': hashed_password,
            'role': 'customer'
        }
        email_data = users_collection.find_one({'email': email})
        if email_data:
            flash('Email already exists')
        else:
            users_collection.insert_one(user)
            return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'role' in session and session['role'] == 'admin':
        if request.method == 'POST':
            service_name = request.form['service_name']
            duration = request.form['duration']
            service = {
                'service_name': service_name,
                'duration': duration
            }
            services_collection.insert_one(service)
            return redirect(url_for('admin_dashboard'))
        services = list(services_collection.find())
        branches = list(branches_collection.find())
        return render_template('admin.html', services=services, branches=branches)
    return redirect(url_for('login'))

@app.route('/add_branch', methods=['POST'])
def add_branch():
    if 'role' in session and session['role'] == 'admin':
        branch_name = request.form['branch_name']
        branch_location = request.form['branch_location']
        opening_time = request.form['opening_time']
        closing_time = request.form['closing_time']
        branch = {
            'name': branch_name,
            'location': branch_location,
            'opening_time': opening_time,
            'closing_time': closing_time
        }
        branches_collection.insert_one(branch)
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

# Initialize the admin user
admin_user = {
    'full_name': 'Thomas N',
    'email': 'thomas.n@compfest.id',
    'phone_number': '08123456789',
    'password': generate_password_hash('Admin123', method='pbkdf2:sha256'),
    'role': 'admin'
}
if not users_collection.find_one({'email': admin_user['email']}):
    users_collection.insert_one(admin_user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)