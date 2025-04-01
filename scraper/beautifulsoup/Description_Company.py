# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 08:17:08 2025

@author: admin
"""
"""
pip install langdetect 
pip install googletrans
"""
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from googletrans import Translator
import logging
import json
import time


# Configuration du module logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extraire_contenu(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        logging.info(f"Envoi de la requête à {url}")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            logging.info("Page récupérée avec succès")
            return response.text
        elif response.status_code == 403:
            logging.error("Erreur 403 : Accès refusé. Le site peut bloquer les robots.")
        elif response.status_code == 404:
            logging.error("Erreur 404 : Page non trouvée.")
        else:
            logging.error(f"Erreur {response.status_code} lors de la récupération de la page.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la requête : {e}")
    return None

def analyser_page(contenu):
    soup = BeautifulSoup(contenu, 'html.parser')
    titre = soup.title.string if soup.title else "Titre non disponible"
    meta_desc = soup.find('meta', {'name': 'description'})
    description = meta_desc['content'] if meta_desc else (
        soup.find('p').get_text(strip=True) if soup.find('p') else "Aucune description disponible"
    )
    langue = detect(description) if description != "Aucune description disponible" else "Langue inconnue"
    return {
        "titre": titre,
        "description": description,
        "langue": langue
    }

def traduire_vers_francais(texte, langue_origine):
    if langue_origine != "en":
        translator = Translator()
        try:
            traduction = translator.translate(texte, src=langue_origine, dest='en').text
            return traduction
        except Exception as e:
            logging.error(f"Erreur lors de la traduction : {e}")
            return texte
    return texte

def generer_description(info):
    titre = info.get("titre", "Titre non disponible")
    description_originale = info.get("description", "Aucune description disponible")
    langue_origine = info.get("langue", "Langue inconnue")
    description_traduite = traduire_vers_francais(description_originale, langue_origine)
    
    description_generale = (
        f"Nom de l'entreprise : {titre}\n"
        f"Langue détectée : {langue_origine}\n"
        f"Description originale ({langue_origine}) : {description_originale}\n"
        f"Description traduite (anglais) : {description_traduite}\n"
    )
    
    return description_generale

def sauvegarder_donnees(data, fichier="resultats.json"):
    try:
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Données sauvegardées dans {fichier}")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde des données : {e}")

def creer_description_entreprise(url):
    contenu = extraire_contenu(url)
    if contenu:
        informations = analyser_page(contenu)
        description = generer_description(informations)
        sauvegarder_donnees(informations)  # Sauvegarde les informations analysées
        return description
    else:
        return "Impossible de générer la description en raison d'une erreur."

# Exemple d'utilisation
if __name__ == "__main__":
    #url = "https://www.cooperators.ca"
    # Autres exemples d'URLs à tester
    url = "https://www.csfoy.ca/accueil"    
    # url = "https://www.theatrerialto.ca/halls"
    # url = "https://labanquise.com/en/"
    # url = "https://www.desjardins.com"
    
    description_entreprise = creer_description_entreprise(url)
    print("Description générée :\n", description_entreprise)
    time.sleep(2)  # Ajout d'un délai entre les requêtes