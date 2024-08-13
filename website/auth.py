from flask import Blueprint, render_template, request, flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email_to_check = request.form.get("login_email")
        passwd_to_check = request.form.get("login_password")
        remember_me = request.form.get("remember_me")
        print(f"Email: {email_to_check}\nPassword: {passwd_to_check}\nif_remember: {remember_me}")

        if email_to_check and passwd_to_check:
            
            user = User.query.filter_by(email=email_to_check).first()
            if user:
                if check_password_hash(user.password, passwd_to_check):
                    flash(f"Successfully logged in. Welcome back {user.name}!", category="success")
                    if remember_me == None:
                        login_user(user, remember=False)
                    else:
                        login_user(user, remember=True)
                    return redirect(url_for("views.home"))
                else:
                    flash("Your password is incorrect.", category="error")
            else:
                flash("There is no user with this Email Address", category="error")

        else:
            flash("Both areas must be filled!", category="error")
    return render_template("login.html")

@auth.route("/logout")
def logout():
    if current_user.is_authenticated:
        flash(f"Successfully Logged Out!. See you soon {current_user.name}", category="success")
        logout_user()
        return redirect(url_for("auth.login"))
    else:
        return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        existing_mail = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()

        if existing_mail:
            flash("An account with this email already exists.", category="error")
        elif existing_username:
            flash("This username is already taken.", category="error")
        elif len(name) < 2:
            flash("Name cannot be shorter than 2 characters.", category="error")
            print("Error 1")
        elif len(surname) <2:
            flash("Surname cannot be shorter than 2 characters.", category="error")
            print("Error 2")            
        elif len(username) < 2:
            flash("Username cannot be shorter than 2 characters.", category="error")
            print("Error 3")
        elif len(email) < 12:
            flash("Email cannot be shorter than 12 characters.", category="error")
            print("Error 4")
        elif len(password) < 7:
            flash("Password cannot be shorter than 7 characters.", category="error")
            print("Error 5")
        elif password != confirm_password:
            flash("Passwords do not match.", category="error")
            print("Error 6")
        else:
            
            print(f"{'-'*10}\nAll Valid\n{'-'*10}")
            
            new_user = User(email=email,
                            name=name,
                            surname=surname,
                            password=generate_password_hash(password, method="pbkdf2:sha256"),
                            username=username)
            
            db.session.add(new_user)
            db.session.commit()

            flash("Successfully Signed Up! Please Login to continue.", category="success")
            return redirect(url_for("auth.login"))


    return render_template("sign-up.html")