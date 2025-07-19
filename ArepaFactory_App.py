from flask import Flask, request, session, render_template_string, redirect
import sqlite3, os, secrets

DB = "products.db"
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(16))

# ----------------------------------------------------------------- Security Headers -----------------------------------------------------------------------
@app.after_request
def add_headers(r):
    r.headers.setdefault("Content-Type", "text/html; charset=utf-8")
    r.headers["X-Frame-Options"] = "DENY"
    r.headers["X-Content-Type-Options"] = "nosniff"
    r.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    r.headers["Content-Security-Policy"] = "default-src 'self'"
    return r

# ------------------------------------------------------------------- CSRF Helpers --------------------------------------------------------------------------
def csrf_token():
    if "tok" not in session:
        session["tok"] = secrets.token_hex(16)
    return session["tok"]

def valid_csrf():
    return request.form.get("csrf") == session.get("tok")

# ----------------------------------------------------------------------- /Add ------------------------------------------------------------------------------
@app.route("/add", methods=["GET", "POST"])
def add():
    msg = ""
    if request.method == "POST" and valid_csrf():
        name  = request.form.get("name", "").strip()
        price = request.form.get("price", "")
        if name and price.replace(".", "", 1).isdigit():
            with sqlite3.connect(DB) as db:
                db.execute("INSERT INTO products(name, price) VALUES(?, ?)",
                           (name, float(price)))
            msg = "Product added!"
        else:
            msg = "Invalid input"
    return render_template_string("""
<!doctype html>
<meta charset=utf-8>
<title>Arepa Factory Shop</title>
<h1>Welcome to the best Arepas Shop</h1>
<img src="{{ url_for('static', filename='logo.jpg') }}" alt="Logo Arepas" width="250">
<h3>Add the Arepa's name and its price..</h3>
<form method=post>
  <input name=name  placeholder="Name">
  <input name=price placeholder="Price" type=number step=0.5>
  <input type=hidden name=csrf value="{{tok}}">
  <button>Add</button>
</form>
<p style="color:green">{{msg}}</p>
<a href="/search">Search products</a>
""", tok=csrf_token(), msg=msg)

# ---------------------------------------------------------------------- /Search -----------------------------------------------------------------------------
@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    rows = []
    if q:
        with sqlite3.connect(DB) as db:
            rows = db.execute(
                "SELECT name, price FROM products WHERE name LIKE ?",
                (f"%{q}%",)
            ).fetchall()
    return render_template_string("""
<!doctype html>
<meta charset=utf-8>
<title>Arepa Factoy Shop</title>
<h1>What Arepa are you Searching?</h1>
<img src="{{ url_for('static', filename='types.jpg') }}" alt="Arepa Types" width="800">
<form>
<input name=q value="{{q}}">
<button>Find</button>
</form>{% for n,p in rows %}<p>{{n}} â€“ ${{"%.2f"|format(p)}}</p>{% else %}
  {% if q %}<p>No matches.</p>{% endif %}{% endfor %}
<a href="/add">Add product</a>
""", q=q, rows=rows)

# ----------------------------------------------------------------------- main -----------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
