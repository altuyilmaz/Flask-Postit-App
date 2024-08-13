from .models import User, Note, Like

def process_notes_with_likes(notes, current_user):
    processed_notes = []
    for note in notes:
        user_liked = any(like.user_id == current_user.id for like in note.likes)
        processed_notes.append((note,user_liked))
    return processed_notes
