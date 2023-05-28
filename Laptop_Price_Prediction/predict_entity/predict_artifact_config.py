from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str

@dataclass
class DataTransformationArtifact:
    feature_store_file_path:str

@dataclass
class DataPreProcessingArtifact:
    feature_store_file_path_data:str
    feature_store_file_path_data_1:str
    feature_store_file_path_null_data:str
    feature_store_file_path_null_data_1:str
    feature_converting_category : str
    

@dataclass
class DataSeprationArtifact:
    feature_store_x_train : str
    feature_store_x_test : str
    feature_store_y_train : str
    feature_store_y_test :str
    scalar_pickle : str


@dataclass
class DataModelArtifact:
    final_models : str