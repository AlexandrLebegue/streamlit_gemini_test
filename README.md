# 📚 AI Book Cover Face Merger

Une application Python qui fusionne intelligemment le visage d'un enfant dans une couverture de livre en utilisant l'IA Google Gemini.

## 🌟 Fonctionnalités

- ✨ **Fusion IA avancée** : Utilise l'API Google Gemini pour une intégration naturelle
- 🎨 **Styles de fusion multiples** : Naturel, artistique, cartoon
- 🖼️ **Interface intuitive** : Interface web Streamlit simple et élégante
- ✅ **Validation d'images** : Vérification automatique de la qualité et compatibilité
- 📥 **Téléchargement facile** : Sauvegarde directe des résultats
- 🔍 **Analyse intelligente** : Suggestions d'amélioration avant fusion

## 🚀 Installation

### Prérequis

- Python 3.8+
- Clé API Google Gemini
- Connexion Internet

### Étapes d'installation

1. **Cloner/télécharger le projet**
   ```bash
   cd ai-book-cover-merger
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer l'API Gemini**
   ```bash
   # Copier le template d'environnement
   cp .env.template .env
   
   # Éditer le fichier .env et ajouter votre clé API
   # GEMINI_API_KEY=votre_clé_api_ici
   ```

4. **Obtenir une clé API Gemini**
   - Visitez [Google AI Studio](https://makersuite.google.com/)
   - Créez un compte et générez une clé API
   - Copiez la clé dans votre fichier `.env`

## 🎯 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Guide d'utilisation

1. **📤 Uploader les images**
   - **Visage enfant** : Photo claire du visage de l'enfant (minimum 100x100px)
   - **Couverture livre** : Image de la couverture de livre (minimum 200x200px)

2. **⚙️ Configurer les options**
   - **Style naturel** : Conservation réaliste du visage
   - **Style artistique** : Adaptation au style illustratif du livre
   - **Style cartoon** : Stylisation pour livres d'enfants

3. **🔍 Analyser (optionnel)**
   - Cliquez sur "Analyser les images" pour obtenir des suggestions
   - Utilisez "Valider les images" pour vérifier la compatibilité

4. **🎨 Générer la fusion**
   - Cliquez sur "Générer la fusion"
   - Attendez quelques instants pour le traitement IA
   - Téléchargez le résultat

### Formats supportés

- **Images d'entrée** : JPEG, PNG
- **Taille maximum** : 10MB par image
- **Format de sortie** : PNG haute qualité

## 📁 Structure du projet

```
ai-book-cover-merger/
├── app.py                      # Application Streamlit principale
├── gemini_client.py           # Client API Gemini
├── create_examples.py         # Générateur d'images d'exemple
├── requirements.txt           # Dépendances Python
├── .env.template             # Template de configuration
├── README.md                 # Documentation
├── architecture.md           # Documentation technique
└── examples/                 # Images d'exemple
    ├── fantasy_adventure.png
    ├── mystery_book.png
    ├── childrens_story.png
    ├── science_fiction.png
    └── sample_child_face.png
```

## 🛠️ Développement

### Architecture technique

L'application suit une architecture modulaire :

- **Interface** : Streamlit pour l'UI web
- **IA** : Google Gemini 2.0 Flash pour la génération d'images
- **Traitement** : Pillow pour le preprocessing des images
- **Configuration** : python-dotenv pour la gestion des variables d'environnement

### API utilisée

```python
# Exemple d'utilisation de l'API Gemini
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=[prompt, face_image, book_image],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE']
    )
)
```

### Créer des images d'exemple

```bash
python create_examples.py
```

## 🔧 Configuration avancée

### Variables d'environnement

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here
MAX_FILE_SIZE_MB=10
SUPPORTED_FORMATS=png,jpg,jpeg
DEFAULT_OUTPUT_FORMAT=png
```

### Optimisation des performances

- **Redimensionnement automatique** : Les images sont optimisées pour l'API
- **Validation en amont** : Vérifications avant traitement
- **Gestion d'erreurs** : Retry logic et messages explicites

## ❗ Dépannage

### Problèmes courants

1. **"GEMINI_API_KEY not found"**
   - Vérifiez que le fichier `.env` existe
   - Confirmez que la clé API est correcte

2. **"API connection failed"**
   - Vérifiez votre connexion Internet
   - Testez la clé API avec le bouton "Test API Connection"

3. **"Image too small/large"**
   - Respectez les dimensions minimales (100x100 pour visage, 200x200 pour livre)
   - Limitez la taille à 10MB maximum

4. **"Failed to generate merged image"**
   - Essayez avec des images de meilleure qualité
   - Changez le style de fusion
   - Vérifiez que les images contiennent bien un visage et une couverture

### Logs et debug

L'application affiche des messages détaillés pour chaque étape. En cas de problème persistant :

1. Vérifiez les messages dans l'interface
2. Testez avec les images d'exemple fournies
3. Consultez la console Python pour plus de détails

## 📝 Licence

Ce projet est à des fins éducatives et de démonstration. Respectez les conditions d'utilisation de Google Gemini API.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📞 Support

Pour toute question ou problème :
1. Consultez cette documentation
2. Vérifiez les exemples fournis
3. Testez la connection API
4. Contactez le support si nécessaire

---

*Créé avec ❤️ en utilisant Streamlit et Google Gemini AI*