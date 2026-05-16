from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# =========================================
# DATABASE
# =========================================

DATABASE = "database.db"

def create_db():

    con = sqlite3.connect(DATABASE)

    cmd = con.cursor()

    cmd.execute("""
    CREATE TABLE IF NOT EXISTS enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        company_name TEXT,
        phone TEXT,
        email TEXT,
        product_interest TEXT,
        requirement TEXT,
        created_date TEXT
    )
    """)

    con.commit()
    con.close()

create_db()

# =========================================
# WEBSITE ROUTES
# =========================================

@app.route('/')
def hello_world():
    return render_template("website.html")

@app.route('/new')
def hello_world1():
    return render_template("new.html")

@app.route("/details")
def details():
    return render_template("details.html")

@app.route("/orion-galaxy-555")
def details2():
    return render_template("details2.html")

@app.route("/orion-galaxy-laser")
def details3():
    return render_template("details3.html")

@app.route("/jewellery-laser")
def details4():
    return render_template("details4.html")

# =========================================
# ENQUIRY FORM SAVE
# =========================================

@app.route("/save-enquiry", methods=["POST"])
def save_enquiry():

    full_name = request.form.get("full_name")
    company_name = request.form.get("company_name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    product_interest = request.form.get("product_interest")
    requirement = request.form.get("requirement")

    con = sqlite3.connect(DATABASE)

    cmd = con.cursor()

    cmd.execute("""
    INSERT INTO enquiries
    (
        full_name,
        company_name,
        phone,
        email,
        product_interest,
        requirement,
        created_date
    )
    VALUES
    (
        ?,?,?,?,?,?,?
    )
    """,
    (
        full_name,
        company_name,
        phone,
        email,
        product_interest,
        requirement,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    con.commit()
    con.close()

    return "Enquiry Saved Successfully"

# =========================================
# ADMIN PANEL
# =========================================

@app.route("/admin")
def admin():

    con = sqlite3.connect(DATABASE)

    con.row_factory = sqlite3.Row

    cmd = con.cursor()

    cmd.execute("""
    SELECT * FROM enquiries
    ORDER BY id DESC
    """)

    data = cmd.fetchall()

    con.close()

    return render_template(
        "admin.html",
        enquiries=data
    )

# =========================================
# MAIL CONFIG
# =========================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'orioninstruments@gmail.com'
app.config['MAIL_PASSWORD'] = 'Amit123'

mail = Mail(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/support")
def support():
    return render_template("support.html")

@app.route("/upload", methods=["POST"])
def upload():

    name = request.form.get("name")
    email = request.form.get("email")
    message_text = request.form.get("message")

    uploaded_file = request.files.get("file")

    filename = ""
    filepath = ""

    if uploaded_file and uploaded_file.filename != "":

        filename = uploaded_file.filename

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        uploaded_file.save(filepath)

    body = f"""
Name: {name}

Email: {email}

Message:
{message_text}
"""

    msg = Message(
        subject="New Support Message",
        sender='orioninstruments@gmail.com',
        recipients=['orioninstruments@gmail.com']
    )

    msg.body = body

    if filepath != "":

        with app.open_resource(filepath) as fp:

            msg.attach(
                filename,
                "application/octet-stream",
                fp.read()
            )

    mail.send(msg)

    return "Email Sent Successfully"

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app.run(debug=True)