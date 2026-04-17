from flask import Flask, request, redirect, session, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, bio TEXT, photo TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS posts (username TEXT, image TEXT, caption TEXT)")

conn.commit()
conn.close()

# UI TEMPLATE
base_style = """
<style>
body { background:#0f172a; color:white; font-family:Arial; text-align:center; }
.box { margin:50px auto; width:300px; padding:20px; background:#1e293b; border-radius:10px; }
input { padding:10px; margin:10px; width:90%; border:none; border-radius:5px; }
button { padding:10px; background:#22c55e; border:none; border-radius:5px; color:white; }
.card { background:#1e293b; margin:10px; padding:10px; border-radius:10px; }
img { width:100px; border-radius:50%; }
</style>
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

    return render_template_string(base_style + """
    <div class="box">
    <h2>Login</h2>
    <form method="POST">
    <input name="username" placeholder="Username"><br>
    <input name="password" type="password" placeholder="Password"><br>
    <button>Login</button>
    </form>
    <a href="/signup">Signup</a>
    </div>
    """)

# SIGNUP
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        bio = request.form["bio"]
        photo = request.form["photo"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?,?)", (user,pw,bio,photo))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template_string(base_style + """
    <div class="box">
    <h2>Signup</h2>
    <form method="POST">
    <input name="username" placeholder="Username"><br>
    <input name="password" placeholder="Password"><br>
    <input name="bio" placeholder="Bio"><br>
    <input name="photo" placeholder="Photo URL"><br>
    <button>Signup</button>
    </form>
    </div>
    """)

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = session["user"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT bio,photo FROM users WHERE username=?", (user,))
    data = c.fetchone()

    c.execute("SELECT * FROM posts")
    posts = c.fetchall()

    conn.close()

    bio = data[0] if data else ""
    photo = data[1] if data else ""

    post_html = ""
    for p in posts:
        post_html += f"""
        <div class="card">
        <h4>{p[0]}</h4>
        <img src="{p[1]}" style="width:200px;border-radius:10px;"><br>
        <p>{p[2]}</p>
        </div>
        """

    return render_template_string(base_style + f"""
    <h2>Welcome {user} 😎</h2>
    <img src="{photo}"><br>
    <p>{bio}</p>

    <div class="box">
    <h3>Add Post</h3>
    <form method="POST" action="/post">
    <input name="image" placeholder="Image URL"><br>
    <input name="caption" placeholder="Caption"><br>
    <button>Post</button>
    </form>
    </div>

    <h3>Feed</h3>
    {post_html}

    <a href="/logout"><button>Logout</button></a>
    """)

# ADD POST
@app.route("/post", methods=["POST"])
def post():
    if "user" not in session:
        return redirect("/")

    user = session["user"]
    img = request.form["image"]
    cap = request.form["caption"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts VALUES (?,?,?)", (user,img,cap))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.run(host="0.0.0.0", port=10000)
