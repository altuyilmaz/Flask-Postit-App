from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User, Note, Like
from . import db
import pytz
from datetime import datetime, timedelta
from .processor import char_len_flash_error_notification, display_notes
views = Blueprint("views", __name__)

@views.route("/")
def home():
    if current_user.is_authenticated:
        note_data,pagination = display_notes(home=True)
        return render_template("home.html", notes=note_data, pagination=pagination)
    else:
        return redirect(url_for("auth.login"))

@views.route("/profiles/<target_username>")
@login_required
def user_gate_keeper(target_username):
    if target_username == current_user.username:   
        return profile()
    else:       
        return checked_profile(target_username)


def profile():
    user,note_data,pagination = display_notes(target_username=current_user.username,home=False)
    return render_template("profile.html", user=user, note_data=note_data, pagination=pagination)

def checked_profile(target_username):
    user,note_data,pagination = display_notes(target_username=target_username,home=False) 
    return render_template("checked-profile.html", user=user, note_like_data=note_data, pagination=pagination)


@views.route("/profiles/create_notes", methods=["POST","GET"])
@login_required
def create_note():
    if request.method == "POST":
        content = request.form.get("content")
        print(content)
        len_checked_content = content.replace(" ", "")
        print(len_checked_content)
        print(len(len_checked_content))
        if not len_checked_content:
            flash("Notes cannot be empty.", category="error")
        elif len(len_checked_content) > 400:
            char_len_flash_error_notification("Length of notes (without spaces)","l","400")
        else:
            new_note = Note(content=content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Congrats! Your new note is added.", category="success")
    return redirect(url_for("views.profile", username=current_user.username))

@views.route("/delete_note/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    if request.method == "POST":
        note = Note.query.get(note_id)
        if note and note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note successfully deleted.", category="success")
        else:
            flash("Something went wrong.", category="error")
    return redirect(url_for("views.profile", username=current_user.username))


@views.route("/like-note/<int:note_id>", methods=["POST","GET"])
def like_note(note_id):
    note = Note.query.get_or_404(note_id)
    like = Like.query.filter_by(user_id=current_user.id, note_id=note_id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        new_like = Like(user_id=current_user.id, note_id=note_id)
        db.session.add(new_like)
        db.session.commit()
        print("liked")
    
    return redirect(request.referrer)

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/contact")
def contact():
    return render_template("contact.html")