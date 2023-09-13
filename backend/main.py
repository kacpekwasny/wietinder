from source import create_app, db, socketio



application = create_app()

def add_users(db):
    from source.models import User
    from werkzeug.security import generate_password_hash
    for email, password, name, bio, sex, target_sex in [
                ("kacper@wp.pl", generate_password_hash("kacper"), "kacper", "jestem kacper :)", "male", "[\"female\"]"),
                ("nata@wp.pl",   generate_password_hash("nata"), "natalia", "jestem natalia :)", "female", "[\"male\"]"),
                ("dawid@wp.pl",  generate_password_hash("dawid"), "dawid", "jestem dawid :)", "male", "[\"female\"]"),
                ("dupaf@wp.pl",  generate_password_hash("dupa"), "DupaF", "jestem dupaf :)", "female", "[\"male\"]"),
                ("dupam@wp.pl",  generate_password_hash("dupa"), "DupaM", "jestem dupam :)", "male", "[\"female\"]"),
            ]:
        try:
            user = User.query.filter_by(email=email).first()
            if user is None:
                db.session.add(User(email=email, password=password, name=name, bio=bio, sex=sex, target_sex=target_sex))
                db.session.commit()
        except Exception as e:
            print("Creating accounts error:", e)

def make_everyone_like_each_other(db):
    from source.models import PossibleMatch, MatchChoice
    for pm in PossibleMatch.query.all():
        pm: PossibleMatch
        pm.user1_choice = MatchChoice.like
        pm.user2_choice = MatchChoice.like
    db.session.commit()

def make_dummy_messages(db):
    from source.models import PossibleMatch, Message
    for pm in PossibleMatch.query.all():
        pm: PossibleMatch
        if len(pm.messages_slice(0, 3)) < 2:
            db.session.add_all([
                Message(author=pm.user1_public_id, possible_match_id=pm.id, message=f"From user1: I have {pm.user1_public_id=}"),
                Message(author=pm.user2_public_id, possible_match_id=pm.id, message=f"From user2: I have {pm.user2_public_id=}"),
            ])
            db.session.commit()

def add_images(db):
    from source.config import UPLOADS_DIR
    from source.models import User
    imgs = list(UPLOADS_DIR.iterdir())
    for u in User.query.all():
        u: User
        if not u.get_images():
            u.set_images([imgs.pop().name])
    db.session.commit()
    
        

if __name__ == '__main__':
    from flask_cors import CORS
    cors = CORS(application, supports_credentials=True)

    with application.app_context():
        db.create_all()
        add_users(db)
        add_images(db)
        make_everyone_like_each_other(db)
        make_dummy_messages(db)

    socketio.run(application, debug=True, port=5000)