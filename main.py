from flask import Flask, request, redirect, render_template_string, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
conn.commit()
conn.close()

# UI TEMPLATE
html = """
<!DOCTYPE html>
<html>
<head>
<title>{{title}}</title>
<style>
body { background:#0f172a; color:white; font-family:Arial; text-align:center; }
.box { margin-top:80px; }
input { padding:10px; margin:10px; border-radius:5px; border:none; }
button { padding:10px 20px; background:#22c55e; border:none; border-radius:5px; color:white; }
a { color:#22c55e; }
.card {
    background:#1e293b;
    padding:20px;
    margin:20px;
    border-radius:10px;
}
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
            return "<h1>Login Failed ❌</h1>"

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

        return "<h1>Signup Success 🎉 <br><a href='/'>Login</a></h1>"

    return render_template_string(html, title="Signup", btn="Signup")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return f"""
    <html>
    <body style="background:#0f172a; color:white; text-align:center; font-family:Arial;">
        <h1>Welcome {session['user']} 🔥</h1>

        <div class="card">
            <h3>Your Dashboard</h3>
            <p>Login successful ✅</p>
        </div>

        <br>
        <a href="/logout"><button>Logout</button></a>
    </body>
    </html>
    """

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run()
