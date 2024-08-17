from flask import flash, request ,redirect, url_for
from flask_login import current_user
from .models import User,Note,Like,Ban
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


def display_notes(home=False, target_username=None, per_page=10):

    page = request.args.get("page",1,type=int)
    filtered_notes = []
    if home:
        all_notes = Note.query.order_by(Note.date.desc()).all()
        for note in all_notes:
            author = User.query.get(note.user_id)
            author_banned_current = Ban.query.filter_by(banned_user_id=current_user.id,banning_user_id=author.id).first()
            current_banned_author = Ban.query.filter_by(banned_user_id=author.id,banning_user_id=current_user.id).first()

        # Filter Banned Users Notes #
            if not (author_banned_current or current_banned_author):
                note.date = note.date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul'))
                user_liked = Like.query.filter_by(user_id=current_user.id, note_id= note.id).first()
                filtered_notes.append({"note":note, "user":author, "user_liked":user_liked})


        # Manual Pagination After Filtration #
        number_of_notes = len(filtered_notes)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_notes = filtered_notes[start:end]

        pagination = {
            "has_next": end < number_of_notes,
            "has_prev": start > 0,
            "next_num": page + 1,
            "prev_num": page - 1,
            "total_pages":  (number_of_notes + per_page -1) // per_page,
            "current_page": page
        }
        return paginated_notes,pagination
    else:
        note_data = []
        user = User.query.filter_by(username=target_username).first()
        if user is None:
            flash("User not found.", category="error")
            return redirect(url_for("views.home"))
        paginated_notes = Note.query.filter_by(user_id=user.id).order_by(Note.date.desc()).paginate(page=page, per_page=per_page)
        for note in paginated_notes.items:
            note.date = note.date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul'))
            user_liked = Like.query.filter_by(user_id=user.id,note_id=note.id).first()
            note_data.append({"note":note,"user":user,"user_liked":user_liked})
        return user, note_data, paginated_notes



def user_is_current_user(username):
    if username != current_user.username:
        flash("You cannot access this page.",category="error")
        return False
    else:
        return True