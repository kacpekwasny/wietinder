from source import create_app

app = create_app()

if __name__ == '__main__':
    from flask_cors import CORS
    cors = CORS(app)

    app.run(debug=True, port=5000)