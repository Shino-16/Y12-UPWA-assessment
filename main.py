from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import user_management as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key


@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")

from flask import Flask, render_template, request, redirect, url_for, session
import userManagement as dbHandler
import pyotp
import pyqrcode
import os
import base64
from io import BytesIO
# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        email = request.form["email"]
        dbHandler.insertUser(username, password, DoB, email)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")
    
    


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)

@app.route('/index.html', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    user_secret = pyotp.random_base32()

totp = pyotp.TOTP(user_secret)  # Generate a QR code for the OTP secret
username = session.get('username', 'default_user')  # Define username
otp_uri = totp.provisioning_uri(name=username, issuer_name="YourAppName")
qr_code = pyqrcode.create(otp_uri)
stream = BytesIO()
qr_code.png(stream, scale=5)
qr_code_b64 = base64.b64encode(stream.getvalue()).decode('utf-8')

if request.method == 'POST':
    otp_input = request.form['otp']  # Fix invalid quotes
    if totp.verify(otp_input):
        return render_template('some_page.html')
        # return redirect(url_for('home'))  # Redirect to home if OTP is valid
    else:
        return "Invalid OTP. Please try again.", 401

return render_template('index.html')  # Ensure proper indentation
