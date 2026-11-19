#============================================================================================
#                             PHASE 3 : Interroger l'API VIES
#============================================================================================

import requests
url = "https://ec.europa.eu/taxation_customs/vies/rest-api/ms/FR/vat/12345678910"
DELAI = 10
#reponse = requests.get(url,timeout=DELAI)
#print(reponse.json())

#eviter que ca se relance en meme temps que les 200 autres 

#============================================================================================
#                                A METTRE DANS LE README!
#Test	Numéro	Résultat
# 1. Numéro connu	FR27552032534	Erreur technique (MS_MAX_CONCURRENT_REQ), à revérifier
# 2. Clé incorrecte	DK73224645	Invalide
# 3. Numéro inventé	FR12345678910	Invalide

# test avec plusieurs url fait dans la boucle sur le notebook nettoyage. J'ai fait deux séries de 20 appels, et j'ai eu des erreurs techniques et un timeout. 

#Un numéro de TVA peut respecter toutes les règles de format et de calcul, mais ne pas correspondre à une entreprise enregistrée. 

#C'est pourquoi on distingue :
#- Validation structurelle : le numéro respecte les règles vérifiées pour son pays.
#- Validation VIES : le numéro est reconnu comme valide dans le système VIES au moment de la vérification.
#============================================================================================

import pandas as pd
import time
import os 
import logging
from datetime import datetime
df = pd.read_csv("starter-kit/API/true_ok.csv")
print(df.head())

# Créer une liste pour stocker les numéros déjà vérifiés
numero_deja_verifiee = []
resultats = []
durees = []

#enregistrer les réponse qui seront dans le csv dans la liste 
if os.path.exists("starter-kit/API/resultats_vies.csv"):
     df_resultats = pd.read_csv("starter-kit/API/resultats_vies.csv")
# Transforme les anciennes réponses du CSV en liste de dictionnaires pour pouvoir y ajouter les nouveaux résultats.
     resultats = df_resultats.to_dict("records")
else:
     resultats =[]

for r in resultats: # Parcourir les anciens résultats enregistrés
    numero_deja_verifiee.append(r["numero_tva_normalise"]) # Récupérer le numéro de TVA complet de chaque résultat

logging.basicConfig(filename="starter-kit/API/collecte_vies.log", level=logging.INFO)
logging.info("Début de la collecte")

for n in df["numero_tva_normalise"].sample(200 , random_state=42):
    if n in numero_deja_verifiee:
        logging.info(f"Numéro déjà vérifié : {n}")
        continue
    url = f"https://ec.europa.eu/taxation_customs/vies/rest-api/ms/{n[0:2]}/vat/{n[2:]}"
    debut = datetime.now()
    try:
         reponse = requests.get(url, timeout=DELAI)
         fin = datetime.now()
         durees.append((fin - debut).total_seconds())
         logging.info(f"Durée de l'appel pour {n} : {durees[-1]} secondes")
         logging.info(f"Code HTTP pour {n} : {reponse.status_code}")
         reponse.raise_for_status()
         donnees_vies = reponse.json()
         erreur = donnees_vies.get("userError")
         if erreur and erreur not in ["INVALID", "VALID"]:
            logging.error(f"Erreur VIES pour {n} : {erreur}")
            time.sleep(10)
            continue
         donnees_vies["numero_tva_normalise"] = n
         resultats.append(donnees_vies) 
         df_resultats = pd.DataFrame(resultats) 
         df_resultats.to_csv("starter-kit/API/resultats_vies.csv", index=False) 
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur de connexion VIES pour {n} : {e}")
    time.sleep(10)

logging.info("Fin de la collecte")
