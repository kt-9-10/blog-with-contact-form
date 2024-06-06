from flask import Flask, render_template, request
import requests
import smtplib
from email.mime.text import MIMEText
import os

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["get", "post"])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        body = f"Name: {name}\nE-mail: {email}\nPhone: {phone}\nMessage:\n{message}"

        my_email = os.environ["MY_EMAIL"]
        password = os.environ["PASSWORD"]

        # MIMETextオブジェクトを作成し、メールの内容を設定する
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = "New Message"
        msg['From'] = my_email
        msg['To'] = my_email

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.send_message(msg)

        return render_template("contact.html", request_method=request.method)

    else:
        return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
