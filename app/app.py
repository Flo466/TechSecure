import os
import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Secure session key from environment
app.secret_key = os.environ["FLASK_SECRET_KEY"]

def get_db_connection():
    """Establishes connection to the MySQL database."""
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
    # Render the homepage
    return render_template("accueil.html")

# ==============================================================================
# ABOUT ROUTE
# ==============================================================================

@app.route("/apropos")
def apropos():
    # Render the about page
    return render_template("apropos.html")

# ==============================================================================
# SERVICES ROUTE
# ==============================================================================

@app.route("/services")
def services():
    # Render the services page
    return render_template("services.html")

# ==============================================================================
# SERVICE DETAIL PAGES
# ==============================================================================

@app.route("/services/cybersecurite")
def cybersecurite():
    # Render the cybersecurity detailed page
    return render_template("cybersecurite.html")

@app.route("/services/supervision-reseau")
def supervision_reseau():
    # Render the network supervision detailed page
    return render_template("supervision_reseau.html")

@app.route("/services/cloud-computing")
def cloud_computing():
    # Render the cloud computing detailed page
    return render_template("cloud_computing.html")

@app.route("/services/administration-systeme")
def administration_systeme():
    # Render the system administration detailed page
    return render_template("administration_systeme.html")

# ==============================================================================
# BRANCHES (FILIALES) ROUTES
# ==============================================================================

@app.route("/filiales")
def filiales():
    db = None
    try:
        # Fetch all branches from the database
        db = get_db_connection()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM filiales;")
        liste_filiales = cursor.fetchall()
        cursor.close()
        return render_template("filiales.html", filiales=liste_filiales)
    finally:
        # Ensure database connection is closed
        if db: db.close()

@app.route("/ajouter_filiale", methods=["GET", "POST"])
def ajouter_filiale():
    # Handle form submission to create a new branch
    if request.method == "POST":
        db = None
        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("INSERT INTO filiales (ville, adresse, responsable, employes, ip_reseau) VALUES (%s, %s, %s, %s, %s)",
                           (request.form['ville'], request.form['adresse'], request.form['responsable'], request.form['employes'], request.form['ip_reseau']))
            db.commit()
            cursor.close()
            flash("Branch added successfully.", "success")
        finally:
            if db: db.close()
        return redirect(url_for("filiales"))
    
    # Render the shared form with no data (Add mode)
    return render_template("ajouter_filiale.html", f=None)

@app.route("/filiale/editer/<int:id>", methods=["GET", "POST"])
def editer_filiale(id):
    db = None
    try:
        # Handle update logic for a specific branch
        db = get_db_connection()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
        if request.method == "POST":
            cursor.execute("UPDATE filiales SET ville=%s, adresse=%s, responsable=%s, employes=%s, ip_reseau=%s WHERE id=%s",
                           (request.form['ville'], request.form['adresse'], request.form['responsable'], request.form['employes'], request.form['ip_reseau'], id))
            db.commit()
            flash("Branch updated successfully.", "success")
            return redirect(url_for("filiales"))
        
        # Fetch current data to pre-fill the shared form
        cursor.execute("SELECT * FROM filiales WHERE id=%s", (id,))
        f = cursor.fetchone()
        cursor.close()
        # Render the shared form with existing data (Edit mode)
        return render_template("ajouter_filiale.html", f=f)
    finally:
        if db: db.close()

@app.route("/filiale/supprimer/<int:id>", methods=["POST"])
def supprimer_filiale(id):
    db = None
    try:
        # Delete a branch record
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM filiales WHERE id=%s", (id,))
        db.commit()
        cursor.close()
        flash("Branch deleted.", "success")
    finally:
        if db: db.close()
    return redirect(url_for("filiales"))

# ==============================================================================
# CONTACT ROUTE
# ==============================================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():
    # Handle contact form submission
    if request.method == "POST":
        db = None
        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("INSERT INTO contacts (nom, prenom, email, telephone, message) VALUES (%s, %s, %s, %s, %s);",
                           (request.form['nom'], request.form['prenom'], request.form['email'], request.form['telephone'], request.form['message']))
            db.commit()
            cursor.close()
            flash("Message sent.", "success")
        finally:
            if db: db.close()
        return redirect(url_for("contact"))
    return render_template("contact.html")

# ==============================================================================
# APP EXECUTION
# ==============================================================================

if __name__ == "__main__":
    # Run the application
    app.run(host="0.0.0.0", port=5000, debug=True)