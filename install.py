import sys
import subprocess

# Vérification de la version de Python
if sys.version_info >= (3, 12):
    print("Attention : Certaines bibliothèques peuvent ne pas être compatibles avec Python 3.12.")
    print("Il est recommandé d'utiliser Python 3.11 pour éviter les problèmes.")

# Installation des dépendances
try:
    subprocess.check_call(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    print("Installation réussie.")
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'installation : {e}")



