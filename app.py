from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.utils import secure_filename
import os
import random

# Initialisation Flask
# Structure : /backend/app.py et /frontend/templates/index.html
app = Flask(__name__, template_folder='../frontend/templates')

# --- CONFIGURATION DES DOSSIERS (Multimédia & Profils) ---
UPLOAD_FOLDER = 'uploads/profiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Autoriser images et vidéos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- CONFIGURATION BASE DE DONNÉES & SÉCURITÉ ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///truthlens_expert_v3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "truthlens-ultra-secure-key-2026" 

db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- MODELE DE DONNÉES (Expert Registry) ---
class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Float, nullable=False)
    matiere = db.Column(db.String(100))
    photo_path = db.Column(db.String(200), default="default.png")

# --- UTILITAIRES ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- LOGIQUE MÉTIER : MOTEUR D'ANALYSE IA ---
def service_ai_engine(protocol):
    """
    Simule une analyse experte complexe au lieu d'un simple Vrai/Faux.
    """
    scenarios = {
        "JUMELLE": {
            "auth": "AUTHENTIQUE (CERTIFIÉ)",
            "emo": random.choice(["STRESSÉ", "AGITÉ", "SOUPÇONNEUX"]),
            "bpm": f"{random.randint(95, 120)} BPM",
            "conf": f"{random.uniform(98.1, 99.9):.2f}%",
            "color": "#1d2ddb"
        },
        "MULTIMEDIA": {
            "auth": "VALIDE (MÉDIA ANALYSÉ)",
            "emo": random.choice(["NEUTRE", "CALME", "SINCÈRE"]),
            "bpm": f"{random.randint(65, 85)} BPM",
            "conf": f"{random.uniform(85.0, 92.5):.2f}%",
            "color": "#bc13fe"
        },
        "XRAY": {
            "auth": "STRUCTURE SUSPECTE DÉTECTÉE",
            "emo": random.choice(["ANXIEUX", "PEUREUX", "DÉFENSIF"]),
            "bpm": f"{random.randint(88, 105)} BPM",
            "conf": f"{random.uniform(92.0, 96.8):.2f}%",
            "color": "#00ff41"
        }
    }
    return scenarios.get(protocol, scenarios["JUMELLE"])

# --- ROUTES OFFICIELLES TRUTHLENS OS ---

@app.route('/')
def home():
    """Charge l'interface Frontend Waoh"""
    return render_template('index.html')

@app.route('/uploads/profiles/<filename>')
def get_uploaded_file(filename):
    """Sert les images/vidéos pour l'interface et le tableau"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/v1/login', methods=['POST'])
def login():
    """Authentification Expert (Postman compatible)"""
    data = request.get_json()
    if not data or data.get("username") != "expert_noor" or data.get("password") != "admin123":
        return jsonify({"msg": "ACCÈS TRUTHLENS REFUSÉ"}), 401
    
    token = create_access_token(identity="expert_noor")
    return jsonify(access_token=token)

@app.route('/v1/etudiants', methods=['POST', 'GET'])
@jwt_required()
def gestion_registre():
    """
    POST: Enregistre une cible (Compatible Postman form-data).
    GET: Retourne le registre complet.
    """
    if request.method == 'POST':
        nom = request.form.get('nom')
        note_str = request.form.get('note')
        matiere = request.form.get('matiere', 'Expertise')
        file = request.files.get('photo')

        if not nom or not note_str:
            return jsonify({"msg": "ERREUR : DONNÉES MANQUANTES"}), 400

        try:
            note = float(note_str)
            filename = "default.png"
            
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{nom}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            nouvelle_cible = Etudiant(
                nom=nom.upper(), 
                note=note, 
                matiere=matiere,
                photo_path=filename
            )
            db.session.add(nouvelle_cible)
            db.session.commit()
            return jsonify({"msg": "CIBLE ENREGISTRÉE", "id": nouvelle_cible.id}), 201
            
        except ValueError:
            return jsonify({"msg": "ERREUR : FORMAT DE NOTE INVALIDE"}), 400

    # Mode GET
    cibles = Etudiant.query.all()
    return jsonify([{
        "id": c.id, 
        "nom": c.nom, 
        "note": c.note, 
        "matiere": c.matiere,
        "photo_url": f"/uploads/profiles/{c.photo_path}"
    } for c in cibles])

@app.route('/v1/scan', methods=['POST'])
@jwt_required()
def execute_scan():
    """
    Déclenche l'expertise approfondie et renvoie les données analytiques.
    """
    data = request.get_json()
    protocol = data.get('protocol', 'JUMELLE')
    
    # Appel au moteur d'analyse experte
    analysis = service_ai_engine(protocol)
    
    return jsonify({
        "status": "ANALYSIS_COMPLETE",
        "protocol": protocol,
        "results": {
            "authenticity": analysis["auth"],
            "emotion": analysis["emo"],
            "heart_rate": analysis["bpm"],
            "confidence": analysis["conf"]
        },
        "ui_config": {
            "theme_color": analysis["color"]
        }
    })

# --- INITIALISATION SYSTÈME ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("--- TRUTHLENS OS : EXPERT ENGINE V3 ACTIVE ---")
    app.run(debug=True, port=5000)
