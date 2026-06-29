import os
from flask import Flask
import MySQLdb

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback-key-dev")

def get_db_connection():
    return MySQLdb.connect(
        host=os.environ.get("DB_HOST", "db_mysql"),
        user=os.environ.get("DB_USER", "techuser"),
        passwd=os.environ.get("DB_PASSWORD", "SecretTechPassword2026"),
        db=os.environ.get("DB_NAME", "techsecure_db")
    )

@app.route("/")
def index():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        cursor.close()
        db.close()
        return f"<h1>TechSecure App</h1><p>Connexion réussie à MySQL ! Version du serveur : {version[0]}</p>"
    except Exception as e:
        return f"<h1>TechSecure App</h1><p>Erreur de connexion à la base : {str(e)}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)