from source import create_app, db

app = create_app()

if __name__ == '__main__':
    from flask_cors import CORS
    cors = CORS(app, supports_credentials=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)