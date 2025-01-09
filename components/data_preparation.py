import re
import pandas as pd
import os, sys
data =  pd.read_csv("/home/marwane/mlops-projects/morocco-appartements-price/artifacts/train.csv", low_memory=False)
import re
import pandas as pd
import os, sys

data = pd.read_csv("/home/marwane/mlops-projects/morocco-appartements-price/artifacts/train.csv", low_memory=False)


class DataPreparationConfig:
    train_prepared_data: str = os.path.join("artifacts", "train_df.csv")


class DataPreparation:
    def __init__(self):
        self.preparation_config = DataPreparationConfig()

    def get_prepared_data(self):
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

        try:
            data = pd.read_csv("/home/marwane/mlops-projects/morocco-appartements-price/artifacts/train.csv", low_memory=False)

            os.makedirs(os.path.dirname(self.preparation_config.train_prepared_data), exist_ok=True)

            numerical_cols = ['price', 'piece', 'rooms', 'bathroom', 'surface', 'étage_du_bien', 'surface_habitable', 'surface_extérieure', 'surface_de_la_parcelle']
            
            # Assuming 'data' is your DataFrame (loaded elsewhere in your code)
            for col_name in numerical_cols:
                data[col_name] = data[col_name].apply(clean_column).apply(to_int)

            # Apply binary conversion
            data = apply_to_binary(df=data)
            return data

        except Exception as e:
            print(f"Error occurred during data preparation: {e}")
            return None


# =============================================

if __name__ == "__main__":
    obj_data_ingest = DataPreparation()
    prepared_data = obj_data_ingest.get_prepared_data()  # Call the function to prepare data
    
    if prepared_data is not None:
        print("Data preparation successful")
        # You can save the prepared data if needed
        prepared_data.to_csv(obj_data_ingest.preparation_config.train_prepared_data, index=False)
    else:
        print("Data preparation failed.")


"""
class DataPreparationConfig:
    #immobilier_prepared_data: str = os.path.join("artifacts", "immobilier_df.csv")
    train_prepared_data: str = os.path.join("artifacts", "train_df.csv")
    #test_prepared_data: str = os.path.join("artifacts", "test_df.csv")


class DataPreparation:
    def __init__(self):
        self.preparation_config = DataPreparationConfig()


    def get_prepared_data(self):
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
                    df[column_name] = df[column_name].apply(to_binary)#.astype(int)
            return df

        
        try:
            os.makedirs(os.path.dirname(os.path.join(self.preparation_config.immobilier_prepared_data)))

            numerical_cols = [ 'price', 'piece', 'rooms', 'bathroom', 'surface', 'étage_du_bien', 'surface_habitable', 'surface_extérieure', 'surface_de_la_parcelle']
            # Assuming 'data' is your DataFrame (loaded elsewhere in your code)
            for col_name in numerical_cols:
                data[col_name] = data[col_name].apply(clean_column).apply(to_int)

            def apply_to_binary(df):
                for column_name in df.columns:
                    if len(df[column_name].value_counts()) == 1:
                        df[column_name] = df[column_name].apply(to_binary)#.astype(int)
                return df
            
            data = apply_to_binary(df=data)
            return data
 
        except Exception as e:
            print(e)
#=============================================
 
if __name__ == "__main__":
    obj_data_ingest = DataPreparation()
    obj_data_ingest.preparation_config()"""
"""
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

# Columns to clean and convert
numerical_cols = [
    'price', 'piece', 'rooms', 'bathroom', 'surface', 'étage_du_bien',
    'surface_habitable', 'surface_extérieure', 'surface_de_la_parcelle'
]

# Assuming 'data' is your DataFrame (loaded elsewhere in your code)
for col_name in numerical_cols:
    data[col_name] = data[col_name].apply(clean_column).apply(to_int)


def to_binary(value):  
    if value == value:
        return 1
    else:
        return 0 

    
def apply_to_binary(df):
    for column_name in df.columns:
        if len(df[column_name].value_counts()) == 1:
            df[column_name] = df[column_name].apply(to_binary)#.astype(int)
    return df
 
data = apply_to_binary(df=data)
# Check the first few rows after transformation
print(data.head(3)) 

""" 
 