
import os
import re
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from dataclasses import dataclass

# DataPreparationConfig for file paths
@dataclass
class DataPreparationConfig:
    train_prepared_data: str = os.path.join("artifacts", "train_df.csv")

# DataTransformationConfig for preprocessor save path
@dataclass
class DataTransformationConfig:
    precessor_obj_file_path = os.path.join("artifacts", "precessor.pkl")

class DataPreparationAndTransformation:
    def __init__(self):
        self.data_preparation_config = DataPreparationConfig()
        self.data_transformation_config = DataTransformationConfig()

    def clean_data(self, df):
        # Define the cleaning function
        def clean_column(value):
            try:
                value = re.sub("[^0-9]", "", value)  # Remove non-numeric characters
            except:
                value = "NaN"
            return value

        # Define the conversion to integer function
        def to_int(value):
            if value not in ["NaN", ""]:
                return float(value)  # Convert to float if value is not NaN or empty
            return float('nan')  # Return NaN if value is NaN or empty

        def to_binary(value):  
            if value == value:
                return 1
            else:
                return 0 
                
        def apply_to_binary(df):
            for column_name in df.columns:
                if len(df[column_name].value_counts()) == 1:
                    df[column_name] = df[column_name].apply(to_binary)
            return df

        # Prepare the data
        try:
            numerical_cols = ['price', 'piece', 'rooms', 'bathroom', 'surface', 'étage_du_bien', 'surface_habitable', 'surface_extérieure', 'surface_de_la_parcelle']
            
            for col_name in numerical_cols:
                df[col_name] = df[col_name].apply(clean_column).apply(to_int)

            # Apply binary conversion where applicable
            df = apply_to_binary(df=df)
            return df
        except Exception as e:
            print(f"Error occurred during data cleaning: {e}")
            return None

    def transform_data(self, df):
        try:
            # Separate categorical & numerical columns
            categorical_cols = ['address', 'description', 'type_de_bien', 'etat', 'état', 'standing', 'livraison1', 'etat_du_bien', 'orientation', 'type_du_sol', 'type_de_terrain', 'constructibilité', 'statut_du_terrain']
            numerical_cols = ['surface', 'piece', 'rooms', 'bathroom', 'étage_du_bien', 'surface_habitable', 'surface_extérieure', 'livraison', 'surface_de_la_parcelle', 'nombre_étages', 'ascenseur', 'sécurité', 'cuisine_équipée', 'four', 'jardin', 'terrasse', 'garage', 'piscine', 'salon_marocain', 'salon_européen', 'antenne_parabolique', 'chauffage_central', 'concierge', 'cheminée', 'climatisation', 'double_vitrage', 'porte_blindée', 'réfrigérateur', 'machine_à_laver', 'micro_ondes', 'chambre_rangement', 'façade_extérieure', 'vue_sur_mer', 'meublé', '3_extras', '7_extras', '6_extras', 'vue_sur_les_montagnes', '9_extras', '4_extras', '17_extras', '5_extras', '2_extras', 'entre_seul', '1_extra', '13_extras', '11_extras', '16_extras', '10_extras', '8_extras', '12_extras']
            
            # Custom ranking for each ordinal feature (Example: categorical column values)
            address_cats = ['Derb Khalid à Casablanca', 'Derb Lahjar à Casablanca', 'Centre Ville à Casablanca', 'El Manar - El Hank à Casablanca', 'Riviera à Casablanca']
            type_de_bien_cats = ['Appartement', 'Terrain', 'Bureau', 'Maison', 'Logement', 'Local commercial', 'Ferme', 'Villa', 'Riad']
            etat_cats = ['À rénover', 'Bon état', 'Nouveau']
            standing_cats = ['Haut standing', 'Moyen standing', 'Économique']
            livraison1_cats = ['Haut standing', 'Moyen standing', 'Économique']
            etat_du_bien_cats = ["Moins d'un an", '1-5 ans', '5-10 ans', '10-20 ans', '20-30 ans', '30-50 ans', '50-70 ans', '70-100 ans', 'Plus de 100 ans']
            orientation_cats = ['Sud', 'Est', 'Ouest', 'Nord']
            type_du_sol_cats = ['Marbre', 'Carrelage', 'Parquet']
            type_de_terrain_cats = ['Lots de villa', 'Industriel', "Groupement d'habitation", "Commercial, Groupement d'habitation", 'Commercial']
            constructibilité_cats = ['R+1', 'R+3', 'R+5', 'R+4', 'R+7']
            statut_du_terrain_cats = ['Loti', 'Non loti']
            cat_columns_categories_list = [address_cats, type_de_bien_cats, etat_cats, standing_cats, livraison1_cats, etat_du_bien_cats, orientation_cats, type_du_sol_cats, type_de_terrain_cats, constructibilité_cats, statut_du_terrain_cats]

            # Numerical pipeline
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="mean")),  # You can adjust strategy as needed
                    ("scaler", StandardScaler())
                ]
            )
            # Categorical pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="constant", fill_value=0)),  # Placeholder for missing values
                    ("ordinalencoder", OrdinalEncoder(categories=cat_columns_categories_list, handle_unknown='use_encoded_value', unknown_value=-1))  # Encoding categorical columns
                ]
            )

            # Preprocessor with ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_cols),
                    ("cat_pipeline", cat_pipeline, categorical_cols)
                ]
            )

            # Apply transformation (fit and transform)
            transformed_data = preprocessor.fit_transform(df)

            return transformed_data

        except Exception as e:
            print(f"Error occurred during data transformation: {e}")
            return None

    def process_data(self, df):
        # First clean the data
        cleaned_data = self.clean_data(df)

        # Then transform the cleaned data
        if cleaned_data is not None:
            transformed_data = self.transform_data(cleaned_data)
            return transformed_data
        else:
            return None

# Example Usage:
data = pd.read_csv("/home/marwane/mlops-projects/morocco-appartements-price/artifacts/immoblier.csv")  # Load your data here
data_preparation_and_transformation = DataPreparationAndTransformation()

# Clean and transform the data
processed_data = data_preparation_and_transformation.process_data(data)
print(processed_data.head())
if processed_data is not None:
    print("Data processed successfully.")
else:
    print("Data processing failed.")
