

from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)


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

# FLASK ROUTE






# MAIL CONFIG

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# YOUR GMAIL
app.config['MAIL_USERNAME'] = 'orioninstruments@gmail.com'

# APP PASSWORD
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

    # SAVE FILE

    if uploaded_file and uploaded_file.filename != "":

        filename = uploaded_file.filename

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        uploaded_file.save(filepath)

    # EMAIL BODY

    body = f"""
Name: {name}

Email: {email}

Message:
{message_text}
"""

    # EMAIL MESSAGE

    msg = Message(
        subject="New Support Message",
        sender='orioninstruments@gmail.com',
        recipients=['orioninstruments@gmail.com']
    )

    msg.body = body

    # ATTACH FILE

    if filepath != "":

        with app.open_resource(filepath) as fp:

            msg.attach(
                filename,
                "application/octet-stream",
                fp.read()
            )

    # SEND EMAIL

    mail.send(msg)

    return "Email Sent Successfully"



if __name__ == "__main__":
    app.run(debug=True)