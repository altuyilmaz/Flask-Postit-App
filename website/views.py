from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User, Note, Like
from . import db
import pytz
from datetime import datetime, timedelta


views = Blueprint("views", __name__)

@views.route("/")
def home():
    if current_user.is_authenticated:
        now = datetime.now()
        two_days_ago = now - timedelta(days=2)
        recent_notes = Note.query.filter(Note.date >= two_days_ago).order_by(Note.date.desc()).all()
        notes_of_users = []
        for note in recent_notes:
            user = User.query.get(note.user_id)
            note.date = note.date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul'))
            user_liked = Like.query.filter_by(user_id=current_user.id, note_id= note.id).first()
            notes_of_users.append({"note": note, "username": user.username, "like":user_liked})

        return render_template("home.html", notes=notes_of_users)
    else:
        return redirect(url_for("auth.login"))

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/contact")
def contact():
    return render_template("contact.html")

@views.route(f"/profiles/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    notes = Note.query.filter_by(user_id=user.id).all()
    note_data = []
    for note in notes:
        note.date = note.date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul'))
        user_liked = Like.query.filter_by(user_id=user.id,note_id=note.id).first()
        note_data.append({"note":note,"user":user,"user_liked":user_liked})
    print(note_data)
    return render_template("profile.html", note_data=note_data)

@views.route("/profiles/create_notes", methods=["POST","GET"])
@login_required
def create_note():
    if request.method == "POST":
        content = request.form.get("content")
        print(content)

        if not content:
            flash("Notes cannot be empty.", category="error")
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

@views.route("/profiles/author/<checked_username>")
@login_required
def checked_profile(checked_username):
    user = User.query.filter_by(username=checked_username).first_or_404()
    if current_user.id == user.id:
        return redirect(url_for("views.profile", username=current_user.username))

    user_notes = Note.query.filter_by(user_id=user.id).order_by(Note.date.desc()).all()
    print("checked user activated.")
    local_tz = pytz.timezone('Europe/Istanbul')
    note_like_data = []
    for note in user_notes:
        note.date = note.date.replace(tzinfo=pytz.utc).astimezone(local_tz)
        checking_user_liked = Like.query.filter_by(user_id=current_user.id,note_id=note.id).first()
        note_like_data.append({"note":note,"checking_user_liked":checking_user_liked})
    return render_template("checked-profile.html", user=user, note_like_data=note_like_data)

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
