import os
import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ["FLASK_SECRET_KEY"]

def get_db_connection():
    """Establishes a connection to the backend MySQL database using environment variables."""
    return MySQLdb.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        passwd=os.environ["DB_PASSWORD"],
        db=os.environ["DB_NAME"],
        charset='utf8mb4'
    )

# ==============================================================================
# HOME ROUTE
# ==============================================================================

@app.route("/")
def accueil():
    """Renders the main landing page."""
    return render_template("accueil.html")

# ==============================================================================
# ABOUT ROUTE
# ==============================================================================

@app.route("/apropos")
def apropos():
    """Renders the About Us page."""
    return render_template("apropos.html")

# ==============================================================================
# SERVICES ROUTE
# ==============================================================================

@app.route("/services")
def services():
    """Renders the corporate IT Services page."""
    return render_template("services.html")

# ==============================================================================
# BRANCHES (FILIALES) ROUTE
# ==============================================================================

@app.route("/filiales")
def filiales():
    """Fetches all subsidiaries from the database and renders the branch dashboard."""
    try:
        db = get_db_connection()
        db.set_character_set('utf8mb4')
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8mb4;')
        cursor.execute('SET CHARACTER SET utf8mb4;')
        
        cursor.execute("SELECT id, ville, adresse, responsable, employes, ip_reseau FROM filiales;")
        liste_filiales = cursor.fetchall()
        
        cursor.close()
        db.close()
        return render_template("filiales.html", filiales=liste_filiales)
    except Exception as e:
        app.logger.error(f"Error fetching branches: {str(e)}")
        return "Internal Server Error", 500

@app.route("/ajouter_filiale")
def ajouter_filiale():
    """Renders the form to add a new subsidiary."""
    return render_template("ajouter_filiale.html")

# ==============================================================================
# CONTACT ROUTE
# ==============================================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Handles both contact form rendering (GET) and secure submission (POST)."""
    if request.method == "POST":
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        email = request.form.get("email")
        telephone = request.form.get("telephone")
        message = request.form.get("message")

        if not all([nom, prenom, email, telephone, message]):
            flash("All fields are required.", "error")
            return redirect(url_for("contact"))

        try:
            db = get_db_connection()
            cursor = db.cursor()
            
            query = """
                INSERT INTO contacts (nom, prenom, email, telephone, message) 
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (nom, prenom, email, telephone, message))
            db.commit()
            cursor.close()
            db.close()
            
            flash("Your message has been securely transmitted. Thank you.", "success")
        except Exception as e:
            app.logger.error(f"Database error during contact submission: {str(e)}")
            flash("An error occurred while processing your request. Please try again later.", "error")
        
        return redirect(url_for("contact"))
        
    return render_template("contact.html")

# ==============================================================================
# APP EXECUTION
# ==============================================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)