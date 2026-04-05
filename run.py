from app import create_app
from app.models import initialize_models

app = create_app()
initialize_models()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
