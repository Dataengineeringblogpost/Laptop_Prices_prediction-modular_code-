from Scrapers.scrape_main import *
from progress.bar import Bar
from Flask_LaptopPricePrediction.app import MyFlaskApp
from Laptop_Price_Prediction.predict_component import data_ingestion
from Laptop_Price_Prediction.predict_component import data_transformation
from Laptop_Price_Prediction.predict_component import data_pre_processing
from Laptop_Price_Prediction.predict_component import data_sepration
from Laptop_Price_Prediction.predict_entity import predict_entity_config
from Laptop_Price_Prediction.predict_component import model_analysis
if __name__ == "__main__":
    try:
        bar = Bar('Processing', max=6)


        # logging.info("Scraping started")
        # scrape_main = main_scrape()
        # data_ingestion_file_path=scrape_main.main()
        # print(data_ingestion_file_path)
        # logging.info("Scraping ended")
        # bar.next()
        data_ingestion_file_path=r"C:\Users\karth\OneDrive\Documents\Laptop_Price_Prediction_Project\artifact\05$d2023_12042611\05$d2023_12042865main_laptop_data.xlsx"
        
        # data_ingestion_file_path=r"C:\Users\karth\OneDrive\Documents\Laptop_Price_Prediction_Project\artifact\05$d2023_12552177\05$d2023_12562976main_laptop_data.xlsx"
        logging.info("Data ingestion started")
        PredictPipelineConfig = predict_entity_config.PredictPipelineConfig(data_ingestion_file_path)
        data_ingestion_config = predict_entity_config.DataIngestionConfig(PredictPipelineConfig=PredictPipelineConfig)
        data_ingestion = data_ingestion.DataIngestion(data_ingestion_config)        
        data_ingestion_artifact = data_ingestion.intitate_data_ingestion()
        logging.info("Data ingestion ended")


        bar.next()

        logging.info("Data Transformation started")
        data_transformation_config = predict_entity_config.DataTransformationConfig(data_ingestion_config)
        data_transformation = data_transformation.DataTransformation(data_ingestion_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.intitate_data_transformation()
        logging.info("Data Transformation ended")

        bar.next()

        logging.info("Data Pre_processing started")
        data_pre_processor_config = predict_entity_config.DataPreProcessConfig(data_transformation_config)
        data_pre_processor =  data_pre_processing.DataPreProcessing(data_transformation_artifact,data_pre_processor_config)
        data_pre_processor_artifact = data_pre_processor.intitate_data_pre_processing()
        logging.info("Data Pre-Processing ended")

        bar.next()
        logging.info("Data Seprated started")
        data_sepration_config = predict_entity_config.DataSeprationConfig(data_pre_processor_config)
        data_sepration = data_sepration.DataSepration(data_pre_processor_artifact,data_sepration_config)
        data_sepration_artifact = data_sepration.initiate_data_sepration() 
        logging.info("Data Seprated ended")
        print(data_sepration_artifact)
        bar.next()
        print("Data is Ready Now Model Creation .....")
        data=input("Do you wanna perform model analysis press y to go ahead or else press any other key:- ")
        if data=='y':

            logging.info("Model_analysis started")
            print("Model_analysis started")
            model_analysis_config = predict_entity_config.ModelAnalysisConfig(data_sepration_config)
            model_analysis = model_analysis.ModelAnalysis(data_sepration_artifact,model_analysis_config)
            model_analysis_artifact = model_analysis.initiate_model_analysis()
            print("Model_analysis ended")
            logging.info("Model_analysis ended")
            print(model_analysis_artifact.final_models)
            model_file_path=model_analysis_artifact.final_models
        else:
            print("File Path :- ",data_sepration_artifact)
            print("Note :- you can create a model the put the file path as a the input ")
        bar.finish()
        
        


        
    except Exception as e:
        logging.debug(str(e))


json_file=model_file_path.rsplit("\\",2)
json_file=json_file[0]+("\\convert_json.json")
sclar_file=json_file[0]+("\\Scalar.pkl")

print("Flask Runing")
app = MyFlaskApp(model_file_path,json_file,sclar_file)
app.run()
