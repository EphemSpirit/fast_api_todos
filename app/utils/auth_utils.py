from app.models import User

def authenticate_user(username: str, password: str, db, context):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False

    if not context.verify(password, user.hashed_password):
        return False

    return True