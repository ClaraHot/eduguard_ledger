# 🔍 TRUTHLENS OS // VIBRANT EDITION
> **Expert Engine V3** - Système d'analyse biométrique et registre sécurisé.

## 📂 Architecture du Projet (EduGuard Ledger)
Le système est structuré pour séparer la logique métier du rendu visuel :

*   **`/backend`** : Cœur du système (Serveur Flask).
    *   `app.py` : Gestion des routes API, logique JWT et moteur IA.
    *   `/instance` : Stockage de la base SQLite `truthlens_expert_v3.db`.
    *   `/uploads/profiles` : Dossier de stockage des photos de profils capturées.
*   **`/frontend`** : Interface utilisateur.
    *   `/templates/index.html` : L'interface Cyberpunk avec effets néon.
*   **`/docs`** : Documentation technique.
    *   `openapi.yaml` : Schéma de l'API pour intégration tierce.
*   **`/scripts`** : Scripts utilitaires.
*   **`.gitignore`** : Configuration pour garder le dépôt léger (exclut `venv`).

---

## 🧠 Protocoles d'Analyse IA (`POST /v1/scan`)
Le moteur IA simule trois niveaux d'expertise approfondie. Utilisez ces protocoles dans le Body JSON de Postman : `{"protocol": "NOM_DU_PROTOCOLE"}`


| Protocole | Usage Expert | Résultats Simulés | Couleur UI |
| :--- | :--- | :--- | :--- |
| **`JUMELLE`** | Analyse de comportement en direct | Stress élevé, Rythme cardiaque 95-120 BPM | Bleu Bio |
| **`MULTIMEDIA`** | Vérification de fichiers média | État neutre/calme, Rythme 65-85 BPM | Violet Pur |
| **`XRAY`** | Détection de structures cachées | État anxieux, Rythme 88-105 BPM | Vert Néon |

---

## 🚀 Guide d'Expertise Postman

### 1️⃣ Authentification (`POST /v1/login`)
*   **URL** : `http://127.0.0`
*   **Body (JSON)** : `{"username": "expert_noor", "password": "admin123"}`
*   **Action** : Copiez le `access_token` reçu.

### 2️⃣ Gestion du Registre (`POST /v1/etudiants`)
*   **Headers** : `Authorization: Bearer <votre_token>`
*   **Body (form-data)** :
    *   `nom` : "NOM_DE_LA_CIBLE"
    *   `note` : "18.5"
    *   `matiere` : "ANALYSE_V3"
    *   `photo` : (Sélectionner un fichier image)

### 3️⃣ Exécution du Scan (`POST /v1/scan`)
*   **Headers** : `Authorization: Bearer <votre_token>`
*   **Body (JSON)** : `{"protocol": "XRAY"}`
*   **Réponse** : Retourne l'authenticité, l'émotion dominante et le BPM.

---

## 🛠️ Installation & Lancement
1. **Activer l'environnement** : `.\venv\Scripts\activate`
2. **Lancer le moteur** : `python backend/app.py`
3. **Accès** : `http://127.0.0.1:5000`

---

## 👨‍💻 Développeur
Système configuré, documenté et déployé par **Noor**.
