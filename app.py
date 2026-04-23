from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback-key')

DB_PATH = 'restaurant.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            guests INTEGER NOT NULL,
            message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    data = request.form
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    date = data.get('date', '').strip()
    time = data.get('time', '').strip()
    guests = data.get('guests', '').strip()
    message = data.get('message', '').strip()

    if not all([name, email, phone, date, time, guests]):
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('index') + '#reserve')

    conn = get_db()
    conn.execute(
        'INSERT INTO bookings (name, email, phone, date, time, guests, message) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (name, email, phone, date, time, int(guests), message)
    )
    conn.commit()
    conn.close()
    flash('Reservation confirmed! We look forward to seeing you.', 'success')
    return redirect(url_for('index') + '#reserve')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.form
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not all([name, email, message]):
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('index') + '#contact')

    conn = get_db()
    conn.execute(
        'INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
        (name, email, message)
    )
    conn.commit()
    conn.close()
    flash('Message sent! We\'ll get back to you soon.', 'success')
    return redirect(url_for('index') + '#contact')

init_db()

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
