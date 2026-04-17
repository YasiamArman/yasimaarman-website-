
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
    }}

    .navbar {{
        background:#111827;
        padding:15px;
        text-align:center;
        font-size:20px;
        font-weight:bold;
    }}

    .container {{
        padding:20px;
    }}

    .card {{
        background:#1e293b;
        padding:15px;
        border-radius:10px;
        margin-bottom:15px;
    }}

    .btn {{
        padding:10px 15px;
        background:#22c55e;
        border:none;
        border-radius:5px;
        color:white;
        cursor:pointer;
    }}

    </style>
    </head>

    <body>

    <div class="navbar">
        🔥 MyApp
    </div>

    <div class="container">
        <h2>Welcome {session['user']} 😎</h2>

        <div class="card">
            <h3>Profile</h3>
            <p>Username: {session['user']}</p>
        </div>

        <div class="card">
            <h3>Activity</h3>
            <p>No posts yet 😅</p>
        </div>

        <a href="/logout"><button class="btn">Logout</button></a>
    </div>

    </body>
    </html>
    """
