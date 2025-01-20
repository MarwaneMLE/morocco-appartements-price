import os 
import sys 
import pandas as pd
import numpy as np

from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
import pickle 
import logging


def save_object(file_path, object):
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(object, file_obj)
        logging.info("Object is saved at {}".format(file_path))

    except Exception as e:
        logging.info('Exception occured while saving object')
        print(e)
    

@dataclass
class DataTransformationConfig:
    precessor_obj_file_path = os.path.join("artifacts", "precessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
 
    def get_transformed_data(self):
        try:
            # Separte categorical & numerical columns
            categorical_cols = ['address', 'description', 'type_de_bien', 'etat', 'état', 'standing', 'livraison1', 'etat_du_bien', 'orientation', 'type_du_sol', 'type_de_terrain', 'constructibilité', 'statut_du_terrain']
            numerical_cols = ['surface', 'piece', 'rooms', 'bathroom', 'étage_du_bien', 'surface_habitable', 'surface_extérieure', 'livraison', 'surface_de_la_parcelle', 'nombre_étages', 'ascenseur', 'sécurité', 'cuisine_équipée', 'four', 'jardin', 'terrasse', 'garage', 'piscine', 'salon_marocain', 'salon_européen', 'antenne_parabolique', 'chauffage_central', 'concierge', 'cheminée', 'climatisation', 'double_vitrage', 'porte_blindée', 'réfrigérateur', 'machine_à_laver', 'micro_ondes', 'chambre_rangement', 'façade_extérieure', 'vue_sur_mer', 'meublé', '3_extras', '7_extras', '6_extras', 'vue_sur_les_montagnes', '9_extras', '4_extras', '17_extras', '5_extras', '2_extras', 'entre_seul', '1_extra', '13_extras', '11_extras', '16_extras', '10_extras', '8_extras', '12_extras']
            
            # Custom ranking for each ordinal feature
            address_cats = ['Derb Khalid à Casablanca', 'Derb Lahjar à Casablanca', 'Centre Ville à Casablanca', 'El Manar - El Hank à Casablanca', 'Riviera à Casablanca', 'Bouchentouf à Casablanca', 'Hay Almasjid à Casablanca', 'Hay Moulay Abdellah à Casablanca', 'Les princesses à Casablanca', 'Garage Allal à Casablanca', 'Ain Borja à Casablanca', 'Casablanca', 'Derb Koréa à Casablanca', 'Hay Al Fath à Casablanca', 'Bourgogne Ouest à Casablanca', 'Quartier Bachkou à Casablanca', 'Anfa à Casablanca', 'Hay Rajaa à Casablanca', 'Ain Diab Extension à Casablanca', 'Hay Arsalan à Casablanca', 'CIL (Hay Salam) à Casablanca', 'City Dar Es Salaam à Casablanca', 'Hay Moulay Rachid 4 à Casablanca', 'Anfa Supérieur à Casablanca', 'Oasis à Casablanca', 'Lissasfa à Casablanca', 'Derb Friha à Casablanca', 'Jamila 4 à Casablanca', 'Hay Idrissia à Casablanca', 'Maârif à Casablanca', 'Jamila 3 à Casablanca', 'Yasmina à Casablanca', 'Foncière à Casablanca', 'Hay Albaraka à Casablanca', 'Quartier Cheminots à Casablanca', 'Derb Al Youssofia à Casablanca', 'La Vilette à Casablanca', 'Hay Moulay Rachid 2 à Casablanca', 'Derb Al kabir à Casablanca', 'Al Qods à Casablanca', 'Tantonville à Casablanca', 'Hay Antaria à Casablanca', 'Jawadi à Casablanca', 'Dar Bouazza à Casablanca', 'Derb Abdellah à Casablanca', 'Hay Palestine à Casablanca', 'Zone Industrielle Oukacha à Casablanca', 'Bournazil à Casablanca', 'Hay Sadri à Casablanca', 'Mandarona à Casablanca', 'Aïn Sebaâ à Casablanca', 'Hay Haddaouia à Casablanca', 'Roches Noires à Casablanca', 'Racine Extension à Casablanca', 'Jamila 7 à Casablanca', 'Derb El Mitre à Casablanca', 'Hay Hassani à Casablanca', 'Oasis sud à Casablanca', 'Habbous à Casablanca', 'Derb Ben Houmane à Casablanca', 'Palmier à Casablanca', 'Ain Chock à Casablanca', 'Polo à Casablanca', 'Hay Alfalah à Casablanca', 'Sidi Belyout à Casablanca', 'Sidi Moumen à Casablanca', 'Hay Chifa à Casablanca', "Triangle d'Or à Casablanca", 'La Gironde à Casablanca', 'Benjdia à Casablanca', 'Nassim 1 à Casablanca', 'Hay Alfarah à Casablanca', 'Bourgogne Est à Casablanca', 'Quartier Al Woroud à Casablanca', 'Sidi El Khadir à Casablanca', 'Plateau (Al Batha) à Casablanca', 'Belvédère à Casablanca', 'Ifriquia à Casablanca', 'Itissal à Casablanca', 'Hay Chrifa à Casablanca', 'Chaâbi à Casablanca', 'Port à Casablanca', 'Alsace Lorraine à Casablanca', 'Al Ahd Al Jadid à Casablanca', 'Derb Omar à Casablanca', 'Dar Lamane à Casablanca', 'Hay Moulay Rachid 3 à Casablanca', 'Sidi Maarouf à Casablanca', 'Moulay Youssef à Casablanca', 'Michouar à Casablanca', 'Anassi à Casablanca', 'Vermont à Casablanca', 'Hay Alamal à Casablanca', 'Tacharouk (Hay Al Walaa) à Casablanca', 'Oulfa à Casablanca', 'Derb Milan (Hay Omar Bnou Alkhattab) à Casablanca', 'Burger à Casablanca', 'Hay Annour à Casablanca', 'Zone Industrielle à Casablanca', 'Franceville à Casablanca', 'Al Azhar à Casablanca', 'Derb Chorfa à Casablanca', 'Hermitage à Casablanca', 'Lahraouiyine à Casablanca', 'Casablanca Finance City à Casablanca', 'Casablanca Marina à Casablanca', 'Hay Adil à Casablanca', 'Hay Al Kodia à Casablanca', 'Lusitania à Casablanca', 'Riad El Ali à Casablanca', 'Hay Mohammadi à Casablanca', 'Derb Douam à Casablanca', 'Derb Loubila à Casablanca', 'Beausite à Casablanca', 'Mabroka à Casablanca', 'Hay Inara à Casablanca', 'La Jonquiere à Casablanca', 'Nassim 2 à Casablanca', 'Hay Al Amal à Casablanca', 'Hay Tissir à Casablanca', 'Derb Al Madania à Casablanca', 'Ville Verte à Bouskoura', 'Hay Moulay Rachid 1 à Casablanca', 'Derb Carlotti à Casablanca', 'La Floride à Casablanca', 'Hay Lmkansa à Casablanca', 'Les Hôpitaux à Casablanca', 'Laymoune à Casablanca', 'Gauthier à Casablanca', 'Longchamps (Hay Al Hanâa) à Casablanca', 'Hay Lamiaa à Casablanca', 'Liberté à Casablanca', 'Sidi Othmane à Casablanca', 'Bernoussi à Casablanca', 'Hay Alfoqara à Casablanca', 'Derb Espagnol à Casablanca', 'Zone Industrielle Moulay Rachid à Casablanca', 'Hay Tasahol à Casablanca', 'Al Andalous à Casablanca', 'Al Hassania à Casablanca', 'Ain Diab à Casablanca', 'Salmia 2 à Casablanca', 'Derb Moulay Cherif à Casablanca', 'Jamila 5 à Casablanca', 'Jamila 6 à Casablanca', 'Derb Salama à Casablanca', 'Val Fleury à Casablanca', 'Sidi Maârouf à Casablanca', 'Jamila 2 à Casablanca', 'Mers Sultan à Casablanca', 'Bel Air à Casablanca', 'Hay Al Qods à Casablanca', 'Racine à Casablanca', 'Hay Hakam à Casablanca', 'Lekrimat à Casablanca', 'Dar Touzani à Casablanca', 'Hay Arrahma à Casablanca', 'Ksar Lebhar à Casablanca', 'Maârif Extension à Casablanca', 'Ancienne Medina à Casablanca', 'Al Osra à Casablanca', 'Les Crêtes à Casablanca', 'Hay Almassira 2 à Casablanca', 'Hay Zobir à Casablanca', 'Hay Tarik à Casablanca', 'Al Madina Aljadida à Casablanca', 'Bouskoura Ville à Casablanca', 'Beauséjour à Casablanca', "Hay M'barka à Casablanca", 'Miamar à Casablanca', 'Hay Al Fadl à Casablanca', 'Ferme Bretonne (Hay Arraha) à Casablanca', 'Al Hadika à Casablanca', 'Californie à Casablanca', 'Ahl Loghlam (Hay Assalam) à Casablanca', 'Almaz à Casablanca', 'Hay Salama à Casablanca', 'Al Farah Dar Essalam à Casablanca', 'Derb Ghalef à Casablanca'] 
            type_de_bien_cats = ['Appartement', 'Terrain', 'Bureau', 'Maison', 'Logement', 'Local commercial', 'Ferme', 'Villa', 'Riad']
            etat_cats = ['À rénover', 'Bon état', 'Nouveau']
            état_cats = ['Finalisé', 'En cours de construction']
            standing_cats = ['Haut standing', 'Moyen standing', 'Économique']
            livraison1_cats = ['Haut standing', 'Moyen standing', 'Économique']
            etat_du_bien_cats = ["Moins d'un an", '1-5 ans', '5-10 ans', '10-20 ans', '20-30 ans', '30-50 ans', '50-70 ans', '70-100 ans', 'Plus de 100 ans']
            orientation_cats = ['Sud', 'Est', 'Ouest', 'Nord']
            type_du_sol_cats = ['Marbre', 'Carrelage', 'Parquet']
            type_de_terrain_cats = ['Lots de villa', 'Industriel', "Groupement d'habitation", "Commercial, Groupement d'habitation", 'Commercial']
            constructibilité_cats = ['R+1', 'R+3', 'R+5', 'R+4', 'R+7']
            statut_du_terrain_cats = ['Loti', 'Non loti']
            cat_columns_categories_list = [address_cats, type_de_bien_cats, etat_cats, état_cats, standing_cats, livraison1_cats, etat_du_bien_cats, orientation_cats, type_du_sol_cats, type_de_terrain_cats, constructibilité_cats, statut_du_terrain_cats]

            # Numerical pipline
            num_pipeline = Pipeline(
            steps = [
                    ("imputer", SimpleImputer()),  # You can adjust strategy here as per your requirement
                    ("scaler", StandardScaler())
                ]  
            )
            # Categorical pipline
            cat_pipeline = Pipeline(
            steps = [
                    ("imputer", SimpleImputer(strategy='constant', fill_value=0)),  # Change to a placeholder like 'missing'
                    ("ordinalencoder", OrdinalEncoder(categories=cat_columns_categories_list, handle_unknown='use_encoded_value', unknown_value=-1)), # Why -1
                ]
            )
            # preprocessor
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline,numerical_cols ),
                    ("cat_pipeline", cat_pipeline, categorical_cols)
                ]
            )
            
            return preprocessor

        except Exception as e:
            print(e)    

    def initialize_data_transformation(self, train_path, test_path):
        try:
            # This data come from data ingestion from artifact dir
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
 
            preprocessing_object = self.get_data_transformation()

            target_column_name = "price"
            drop_columns = [target_column_name, "id"]
             
            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = test_df[target_column_name]

            input_feature_train_arr = preprocessing_object.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_object.transform(input_feature_test_df)

            #logging.info("Preprocesing in applyed on train and test data")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_object_file_path,
                object=preprocessing_object
            )
            #logging.info("The preprocessing pickle file is saved")

            return (
                train_arr,
                test_arr
            )
        
        except Exception as e:
            logging.info("Exception occured  in the initiate_dataframe")
            print(e)