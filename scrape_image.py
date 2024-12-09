from selenium.webdriver import ActionChains 

# Permet d'utiliser le WebDriver pour contrôler un navigateur web
from selenium import webdriver

 # Permet de gérer le service ChromeDriver (non utilisé ici, mais peut être nécessaire dans certains cas)
from selenium.webdriver.chrome.service import Service 
# Permet d'interagir avec le système d'exploitation, par exemple pour gérer les chemins de fichiers
import os
# Permet de localiser des éléments sur la page web
from selenium.webdriver.common.by import By
# Permet d'ajouter des pauses dans le script (utile pour éviter des erreurs dues à des actions trop rapides)
import time
import pandas as pd  


# Création d'une instance de ChromeOptions pour personnaliser les options du navigateur
options = webdriver.ChromeOptions()

# Ajout d'une option pour exclure les messages de logging de Chrome
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialisation du driver Chrome avec les options définies
driver = webdriver.Chrome(options=options)

# si vous ajouter le "executable_path" dans le cas au vous utilisez un ancie version
#driver = webdriver.Chrome(executable_path=path_chomedriver, options=options)

# Le lien du site ascraper
url = "https://jobdiali.com/category/haut-commissariat-au-plan/"

# Ouverture du lien spécifiée dans la variable 'lien'
driver.get(url)

# Pause de 10 secondes
time.sleep(10)
d