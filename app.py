from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, name TEXT, amount INTEGER)")
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        amount = request.form.get("amount")

        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (name, amount))
        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    data = cur.fetchall()
    conn.close()

    content = """
<!DOCTYPE html>
<html>
<head>
    <title>Expense Tracker</title>
    <style>
        body {
            font-family: 'Segoe UI';
            background: linear-gradient(to right, #667eea, #764ba2);
            margin: 0;
            padding: 0;
            text-align: center;
            color: white;
        }
        .container {
            background: white;
            color: black;
            width: 400px;
            margin: 60px auto;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.3);
        }
        input {
            padding: 10px;
            width: 40%;
            margin: 5px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            padding: 10px 15px;
            border: none;
            background: #667eea;
            color: white;
            border-radius: 8px;
            cursor: pointer;
        }
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
        }
    </style>
</head>
<body>

<div class="container">
 <h1>💰 Expense Tracker - CI/CD Working</h1>
    <form method="POST">
        <input name="name" placeholder="Expense">
        <input name="amount" placeholder="Amount">
        <button>Add</button>
    </form>

    <table>
        <tr><th>Name</th><th>Amount</th></tr>
"""

    for row in data:
        content += f"<tr><td>{row[1]}</td><td>₹{row[2]}</td></tr>"

    content += """
    </table>
</div>

</body>
</html>
"""
    return content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
