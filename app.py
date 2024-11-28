import pyodbc
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure database connection
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=;'  # Replace with your Windows host IP
        'DATABASE=PunchCardSystem;'
        'Trusted_Connection=yes;'     # Uses Windows Authentication
    )
    return conn



@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT first_name, last_name, employee_role FROM Employee WHERE username = ? AND password_hash = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        return redirect(url_for('dashboard', first_name=user[0], last_name=user[1], role=user[2]))
    else:
        flash('Invalid username or password!')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    role = request.args.get('role')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT week_id, week_ending_day, total_hours, overtime, weighted_hours FROM WeekLog WHERE employee_id = (SELECT employee_id FROM Employee WHERE first_name = ? AND last_name = ?)"
    cursor.execute(query, (first_name, last_name))
    week_logs = cursor.fetchall()
    
    return render_template('dashboard.html', first_name=first_name, last_name=last_name, role=role, week_logs=week_logs)

if __name__ == '__main__':
    app.run(debug=True)
