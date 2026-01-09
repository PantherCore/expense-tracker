from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- Database ----------
def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------- Routes ----------
@app.route('/')
def index():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
    conn.close()
    return render_template('index.html', expenses=expenses, total=total or 0)

@app.route('/add', methods=['POST'])
def add_expense():
    title = request.form['title']
    amount = request.form['amount']

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (title, amount) VALUES (?, ?)",
        (title, amount)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# ---------- Run ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
