from flask import flash, request
from flask_login import current_user
from .models import User,Note,Like
from typing import Literal
import pytz


def char_len_flash_error_notification(error_relation: str,
                                    type: Literal["s","short","shorter","l","long","longer"],
                                    char_len: str):
    if type == "s" or type == "short" or type == "shorter":
        notified_issue = "shorter"
    elif type == "l" or type == "long" or type == "longer":
        notified_issue = "longer"

    error_string = f"{error_relation.capitalize()} cannot be {notified_issue} than {char_len} characters."

    print(f"Error: '{error_relation}' : '{notified_issue}' : '{char_len}'")

    return flash(error_string, category="error")


def display_notes(home=False, target_username=None):

    page = request.args.get("page",1,type=int)
    note_data = []
    if home:
        paginated_notes = Note.query.order_by(Note.date.desc()).paginate(page=page,per_page=10)
        for note in paginated_notes.items:
            user = User.query.get(note.user_id)
            note.date = note.date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul'))
            user_liked = Like.query.filter_by(user_id=current_user.id, note_id= note.id).first()
            note_data.append({"note":note, "username":user.username, "like":user_liked})
        return note_data, paginated_notes
    else:
        user = User.query.filter_by(username=target_username).first_or_404()
        paginated_notes = Note.query.filter_by(user_id=user.id).order_by(Note.date.desc()).paginate(page=page, per_page=10)
        for note in paginated_notes.items:
            note.date = note.date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul'))
            user_liked = Like.query.filter_by(user_id=user.id,note_id=note.id).first()
            note_data.append({"note":note,"user":user,"user_liked":user_liked})
        return user, note_data, paginated_notes
            