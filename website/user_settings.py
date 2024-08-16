from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User
from . import db
from .processor import char_len_flash_error_notification

user_settings = Blueprint("user_settings",__name__)

@user_settings.route("/profiles/<username>/preferences", methods=["POST","GET"])
@login_required
def preferences(username):
    if username != current_user.username:
        flash("You cannot access this page.",category="error")
        return redirect(url_for("views.home"))
    else:
        return "<h1>Function Works</h1>"

@user_settings.route("/profiles/<username>/edit-profile", methods = ["POST","GET"])
def edit_profile(username):
    return "<h1>Function Works</h1>"

@user_settings.route("/profiles/<username>/change_password", methods = ["POST","GET"])
def change_password(username):
    return "<h1>Function Works</h1>"

@user_settings.route("/profiles/<username>/account-history", methods = ["POST","GET"])
def account_history(username):
    return "<h1>Function Works</h1>"

@user_settings.route("/profiles/<username>/language", methods = ["POST","GET"])
def language(username):
    return "<h1>Function Works</h1>"

@user_settings.route("/profiles/<username>/account-freeze", methods = ["POST","GET"])
def account_freeze_delete(username):
    return "<h1>Function Works</h1>"
