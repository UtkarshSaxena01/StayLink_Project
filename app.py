from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'a3d1f49158eea841cdec9975c50345de5212bda95a141ff9'  # Secure random string

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'vd8DYewD@1',
    'database': 'hotel_booking'
}

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# ---------------------- AUTH ROUTES ---------------------- #
@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, password))
            conn.commit()
        except mysql.connector.errors.IntegrityError:
            flash("Email already registered.")
            return redirect('/register')
        finally:
            conn.close()

        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect('/admin')
        else:
            flash("Invalid credentials. Please try again.")
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------------- BOOKING ROUTES ---------------------- #
@app.route('/index_user')
def index_user():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    conn.close()
    return render_template('index_user.html', bookings=bookings)

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    check_in = request.form['check_in']
    check_out = request.form['check_out']
    guests = request.form['guests']
    type_of_room = request.form['type_of_room']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (name, email, check_in, check_out, guests, type_of_room) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, email, check_in, check_out, guests, type_of_room)
    )
