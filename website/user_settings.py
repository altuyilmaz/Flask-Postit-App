from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User
from . import db
from .processor import char_len_flash_error_notification

user_settings = Blueprint("user_settings",__name__)

def user_is_current_user(username):
    if username != current_user.username:
        flash("You cannot access this page.",category="error")
        return False
    else:
        return True

@user_settings.route("/profiles/<username>/settings")
@login_required
def settings(username):
    if user_is_current_user(username=username):
        return render_template("settings.html")
    else:
        return redirect(url_for("views.home"))
    
@user_settings.route("/profiles/<username>/settings/edit-profile",methods=["POST", "GET"])
def edit_profile(username):
    if user_is_current_user(username=username):
        if request.method == "POST":
            fields_empty = True
            change_made = False
            changes = {}
            for key, value in request.form.items():
                if value:
                    fields_empty = False
                    if value != getattr(current_user, key):
                        if key == "username" and User.query.filter_by(username=value).first() != None:
                                flash("This username is already taken.",category="error")
                                return redirect(url_for('user_settings.settings', username=current_user.username))
                        elif key == "email" and User.query.filter_by(email=value).first() != None:
                                flash("This email is already taken.",category="error")
                                return redirect(url_for('user_settings.settings', username=current_user.username))
                        else:
                            print(f"Value to change: {key} will be {value}") 
                            changes[key] = value
                            setattr(current_user,key,value)
                            change_made = True

        
    
            if change_made:
                text = ""
                for key, value in changes.items():
                    text += f"{key.capitalize()} is changed to: <strong>{value}</strong><br>"
                
                flash(f"{text}",category="success")

                db.session.commit()
            elif fields_empty:
                flash("All fields empty. Nothing edited.", category="error")
            else:
                flash("All values are the same. No change made.", category="error")
            
            return redirect(url_for('user_settings.settings', username=current_user.username))
    else:
        print("penetration attempt")
        return redirect(url_for("auth.login"))
