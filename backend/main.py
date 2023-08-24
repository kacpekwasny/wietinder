from source import create_app, db

app = create_app()

def add_users(db):
    from source.models import User
    from werkzeug.security import generate_password_hash
    for email, password, name, bio, sex, target_sex in [
                ("kacper@wp.pl", generate_password_hash("kacper"), "kacper", "jestem kacper :)", "male", "[\"female\"]"),
                ("nata@wp.pl",   generate_password_hash("nata"), "natalia", "jestem natalia :)", "female", "[\"male\"]"),
                ("dawid@wp.pl",  generate_password_hash("dawid"), "dawid", "jestem dawid :)", "male", "[\"female\"]"),
            ]:
        try:
            user = User.query.filter_by(email=email).first()
            if user is None:
                db.session.add(User(email=email, password=password, name=name, bio=bio, sex=sex, target_sex=target_sex))
                db.session.commit()
        except Exception as e:
            print("Creating accounts error:", e)

if __name__ == '__main__':
    from flask_cors import CORS
    cors = CORS(app, supports_credentials=True)

    with app.app_context():
        db.create_all()
        add_users(db)

    app.run(debug=True, port=5000)