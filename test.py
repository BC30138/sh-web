from flask import Flask, request
from flask_login import LoginManager, current_user, login_required
from warrant import Cognito

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

USER_POOL_ID = "eu-central-1_R7kMPFbB3"
CLIENT_ID = "35g94vf37ro8d2m8ab1nilld18"


@login_manager.request_loader
def load_user_from_request_header(request):
    try:
        access_token = request.headers["Authorization"]
        cognito = Cognito(USER_POOL_ID, CLIENT_ID, access_token)
        username = cognito.get_user()._metadata.get("username")
        if username is None:
            return None
        return "yeah"
    except Exception as e:
        return None


@app.route("/this-page-needs-login")
@login_required
def page_with_login():
    return f"Logged in! Hi, {current_user.username}"


if __name__ == '__main__':
    app.run(debug=True)
