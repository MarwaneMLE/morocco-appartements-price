from data_ingestion import DataIngestion
from data_preparation import DataPreparation
from data_transformation import DataTransformation



class TrainingPipeline:

    def start_data_ingestion(self):
        try:
            object = DataIngestion()

            train_data_path, test_data_path = object.initiate_data_ingestion()
            return train_data_path, test_data_path
        except Exception as e:
            print(e)
    
    def start_data_preparation(self):
        try:
            data_preparation = DataPreparation()

            train_data_path, test_data_path = data_preparation.get_prepared_data()
            return train_data_path, test_data_path
        except Exception as e:
            print(e)


    def start_data_transformation(self, train_data_path, test_data_path):
        try:
            data_transformation = DataTransformation()
            train_arr, test_arr = data_transformation.initialize_data_transformation(train_data_path, test_data_path)
            return train_arr, test_arr
        except Exception as e:
            print(e)
        


object = DataIngestion()

train_path, test_path = object.initiate_data_ingestion()
data_preparation = DataPreparation()
 
#train_prepared_data = data_preparation.get_prepared_data()
#test_prepared_data = data_preparation.get_prepared_data()
 
data_transformation = DataTransformation()
train_arr, test_arr = data_transformation.initialize_data_transformation(train_path, test_path)
print(train_arr, test_arr)


"""
model_trainer_object = ModelTrainer()
model_trainer_object.initiate_model_trainig(train_arr, test_arr)

# Evaluation the model
model_trainer_object = ModelTrainer()
model_trainer_object.initiate_model_trainig(train_arr, test_arr)

model_eval_object = ModelEvaluation()
model_eval_object.initiate_model_evaluation(train_arr, test_arr) 
"""