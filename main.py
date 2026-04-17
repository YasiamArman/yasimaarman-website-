from flask import Flask, request, redirect, session, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
conn.commit()
conn.close()

# COMMON UI
html = """
<!DOCTYPE html>
<html>
<head>
<title>{{title}}</title>
<style>
body { background:#0f172a; color:white; font-family:Arial; text-align:center; }
.box { margin-top:100px; }
input { padding:10px; margin:10px; border-radius:5px; border:none; }
button { padding:10px 20px; background:#22c55e; border:none; border-radius:5px; color:white; }
a { color:#22c55e; }
</style>
</head>
<body>
<div class="box">
<h2>{{title}}</h2>
<form method="POST">
<input name="username" placeholder="Username"><br>
<input name="password" type="password" placeholder="Password"><br>
<button type="submit">{{btn}}</button>
</form>
<br>
<a href="/signup">Signup</a> | <a href="/">Login</a>
</div>
</body>
</html>
"""

# LOGIN
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pw))
        result = c.fetchone()
        conn.close()

        if result:
            session["user"] = user
            return redirect("/dashboard")
        else:
            return "Login Failed ❌"

    return render_template_string(html, title="Login", btn="Login")

# SIGNUP
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?)", (user,pw))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template_string(html, title="Signup", btn="Signup")

# DASHBOARD (WITH PHOTO 🔥)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return f"""
    <html>
    <head>
    <style>
    body {{
        margin:0;
        font-family: Arial;
        background:#0f172a;
        color:white;
        text-align:center;
    }}

    .navbar {{
        background:#111827;
        padding:15px;
        font-size:20px;
        font-weight:bold;
    }}

    .container {{
        padding:20px;
    }}

    .profile {{
        margin-top:20px;
    }}

    .profile img {{
        width:120px;
        border-radius:50%;
        border:3px solid #22c55e;
    }}

    .card {{
        background:#1e293b;
        padding:15px;
        border-radius:10px;
        margin:15px;
    }}

    .btn {{
        padding:10px 15px;
        background:#22c55e;
        border:none;
        border-radius:5px;
        color:white;
    }}

    </style>
    </head>

    <body>

    <div class="navbar">🔥 MyApp</div>

    <div class="container">

        <div class="profile">
            <img src="https://picsum.photos/200">
        </div>

        <h2>Welcome {session['user']} 😎</h2>

        <div class="card">
            <p>Username: {session['user']}</p>
        </div>

        <a href="/logout"><button class="btn">Logout</button></a>

    </div>

    </body>
    </html>
    """

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
