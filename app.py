import os
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.discord import make_discord_blueprint, discord

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersekrit")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Remove in production

discord_bp = make_discord_blueprint(
    client_id=os.getenv("DISCORD_CLIENT_ID"),
    client_secret=os.getenv("DISCORD_CLIENT_SECRET"),
    redirect_to="home",
)
app.register_blueprint(discord_bp, url_prefix="/login")

@app.route("/")
def home():
    if not discord.authorized:
        return redirect(url_for("discord.login"))
    resp = discord.get("/api/v6/users/@me")
    user_info = resp.json()
    return render_template("index.html", user_info=user_info)

@app.route("/logout")
def logout():
    token = discord_bp.token["access_token"]
    requests.post(
        "https://discord.com/api/v6/oauth2/token/revoke",
        data={"token": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=(os.getenv("DISCORD_CLIENT_ID"), os.getenv("DISCORD_CLIENT_SECRET")),
    )
    del discord_bp.token
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
