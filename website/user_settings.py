from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User
from . import db
from .processor import char_len_flash_error_notification

user_settings = Blueprint("user_settings",__name__)

@user_settings.route("/profiles/<username>/change-name", methods=["POST","GET"])
@login_required
def change_name(username):
    if username != current_user.username:
        flash("You cannot access this page.",category="error")
        return redirect(url_for("views.home"))
    else:
        return "<h1>Function Works</h1>"
