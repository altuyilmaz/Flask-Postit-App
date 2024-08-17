from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User, Ban
from . import db
from .processor import char_len_flash_error_notification, user_is_current_user

user_settings = Blueprint("user_settings",__name__)


@user_settings.route("/profiles/<target_username>/ban-user", methods=["POST","GET"])
def ban_user(target_username):
    return_back_settings = redirect(url_for('user_settings.settings', username=current_user.username)+'#preferences')
    if request.method == "POST":

        user_to_ban = User.query.filter_by(username=target_username).first()
        if user_to_ban:

            existing_ban = Ban.query.filter_by(banned_user_id=user_to_ban.id, banning_user_id=current_user.id).first()
            if existing_ban:
                flash("You already banned this user.", category="error")
                return return_back_settings
            else:
                try:
                    new_ban = Ban(banned_user_id=user_to_ban.id,banning_user_id=current_user.id)
                    print(f"New Ban: \n Banner: {new_ban.banning_user_id} Banned: {new_ban.banned_user_id}") #debugger
                    db.session.add(new_ban)
                    db.session.commit()
                    flash(f"User: <strong>{target_username}</strong> is successfully banned.", category="info")
                except Exception as e:
                    db.session.rollback()
                    print("Error: ",e)
                    flash("An unexpected error occurred. Please try again later.", category="error")
                return return_back_settings

        else:
            flash("User not found.",category="error")
            return return_back_settings


    else:
        print("something went wrong.")
        return 

@user_settings.route("/profiles/<username>/settings")
@login_required
def settings(username):
    if user_is_current_user(username=username):
        return render_template("settings.html")
    else:
        return redirect(url_for("views.home"))
    
@user_settings.route("/profiles/<username>/settings/edit-profile",methods=["POST", "GET"])
def edit_profile(username):
    return_back_settings = redirect(url_for('user_settings.settings', username=current_user.username))
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
                            return return_back_settings
                        elif (key =="username" or key== "name" or key == "surname") and len(value) < 2:
                            char_len_flash_error_notification(key,"s","2")
                            return return_back_settings
                        elif (key =="username" or key== "name" or key == "surname") and len(value) > 20:
                             char_len_flash_error_notification(key,"l","20")
                             return return_back_settings
                        
                        elif key == "email" and User.query.filter_by(email=value).first() != None:
                            flash("This email is already taken.",category="error")
                            return return_back_settings
                        elif key == "email" and len(value) < 12:
                            char_len_flash_error_notification(key,"s","12")
                            return return_back_settings
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
