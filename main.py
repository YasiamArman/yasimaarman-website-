from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# DATABASE CREATE
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
conn.commit()
conn.close()

# HTML
html = """
<!DOCTYPE html>
<html>
<head>
<title>Mini App</title>
<style>
body { background:#0f172a; color:white; text-align:center; font-family:Arial; }
.box { margin-top:100px; }
input { padding:10px; margin:10px; border-radius:5px; }
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
            return f"<h1>Welcome {user} 🔥</h1>"
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

if __name__ == "__main__":
    app.run()
