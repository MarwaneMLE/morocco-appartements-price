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

# Permet de travailler avec des DataFrames (utile pour structurer les données collectées)
import pandas as pd  




def scrape_information(list_link_appartements):
    """ Methode to scrape data from given list of links"""
    options = webdriver.ChromeOptions()

    # Ajout d'une option pour exclure les messages de logging de Chrome
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Initialisation du driver Chrome avec les options définies
    driver = webdriver.Chrome(options=options)
    
    appartements_infos = []
    for i in range(len(list_link_appartements)):
        
        driver = webdriver.Chrome(options=options)
        driver.get(list_link_appartements[i])
        time.sleep(5) 


        try:
            appartement_features = driver.find_element(By.CLASS_NAME, "mainInfoProp")#[0].text
        except:
            appartement_features = None
        try:
            price = appartement_features.find_element(By.CLASS_NAME, "orangeTit").text
        except:
            price = None
        try:
            aire = appartement_features.find_elements(By.CLASS_NAME, "adDetailFeature")[0].text
        except:
            aire = None
        try:
            piece = appartement_features.find_elements(By.CLASS_NAME, "adDetailFeature")[1].text
        except:
            piece = None
        try:
            rooms = appartement_features.find_elements(By.CLASS_NAME, "adDetailFeature")[2].text
        except:
            rooms = None
        try:
            bathroom = appartement_features.find_elements(By.CLASS_NAME, "adDetailFeature")[3].text
        except:
            bathroom = None
        try:
            address = appartement_features.find_element(By.CLASS_NAME, "greyTit").text
        except:
            address = None

        try:
            appartement_more_infos = driver.find_element(By.CLASS_NAME, "blockProp")
        except:
            appartement_more_infos = None
        try:
            more_infos = appartement_more_infos.find_element(By.CLASS_NAME, "searchTitle").text
        except:
            more_infos = None 
        try:    
            descriptions = appartement_more_infos.find_elements(By.TAG_NAME, "p")
            description = ["".join(descrip.text) for descrip in descriptions]
            description = "".join(description)
        except:
            description = None
        try:
            more_features = driver.find_element(By.CLASS_NAME, "caractBlockProp")
        except:
            more_features = None
        try:
            list_features1 = more_features.find_elements(By.CLASS_NAME, "adMainFeature")
        except:
            list_features1=None
        try:
            list_values1 = more_features.find_elements(By.CLASS_NAME, "adMainFeature")
        except:
            list_values1=None
        try:
            feat_infos_dic1 = {}
            for i in range(len(list_features1)): 
                feat_infos_dic1[f"{list_features1[i].text}"] = f"{list_features1[i].text}"
        except:
            feat_infos_dic1 = None
        
        more_features = driver.find_element(By.CLASS_NAME, "caractBlockProp")
        list_features2 = more_features.find_elements(By.CLASS_NAME, "adFeature")
        #list_values2 = more_features.find_elements(By.CLASS_NAME, "adFeature")
        
        try:
            feat_infos_dic2 = {}
            for i in range(len(list_features2)): 
                feat_infos_dic2[f"{list_features2[i].text}"] = list_features2[i].text
        except:
            feat_infos_dic2 = None
        values = [price, aire, piece, rooms, bathroom, address, more_infos, description, feat_infos_dic1, feat_infos_dic2]
        appartements_infos.append(values)


    features = ["price", "aire", "piece", "rooms", "bathroom", "address", "more_infos", "description", "feat_infos_dic1", "feat_infos_dic2"]
    df = pd.DataFrame(data=appartements_infos, columns=features)
    return df  

df_link = pd.read_csv("link-file.csv") 
immobier_links = df_link.link.values.tolist()


data_100 = scrape_information(list_link_appartements=immobier_links[:100])

data_100.to_csv("casablanca-immobiliers-0-200.csv", index=False)
 