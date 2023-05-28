
from flask import Flask,request,jsonify,render_template
import pickle
import json
import numpy as np
import pandas  as pd
class MyFlaskApp:
    def __init__(self,model_file_path,json_file,sclar_file):
        self.model_file_path = model_file_path
        self.json_file  = json_file
        self.sclar_file=sclar_file
        self.app = Flask(__name__)
        self.app.add_url_rule("/", view_func=self.index,methods=["GET",'POST'])
        self.app.add_url_rule('/predict_api', view_func=self.predict, methods=['POST'])



    def index(self):
        encodings = ['utf-8-sig', 'latin-1', 'cp1252']

        # Attempt to open the file with different encodings
        for encoding in encodings:
            try:
                with open(self.json_file, 'r', encoding=encoding) as file:
                    json_data = json.load(file)
                break
            except UnicodeDecodeError:
                continue

        list_of_columns=['brand_name','processor_brand','ram','os','storage']
      
        processor_brand=pd.DataFrame(json_data['processor_brand'])
        brand_name = pd.DataFrame(json_data['brand_name'])
        memory = pd.DataFrame(json_data['ram'])
        storage = pd.DataFrame(json_data['storage'])
        os = pd.DataFrame(json_data['os'])
        return render_template('index.html',processor_brand=processor_brand,brand_name=brand_name,memory=memory,storage=storage,os=os)
    

    def predict(self):
        li=[]
        prediction=36000
        pre=1000
   
        Brand_Name=request.form.get('brand_name')
        li.append(int(Brand_Name))
        processor_brand=request.form.get('processor_brand')
        li.append(int(processor_brand))
        ram=request.form.get('ram')
        li.append(int(ram))
        os=request.form.get('os')
        li.append(int(os))
        storage=request.form.get('storage')
        li.append(int(storage))
        
        print(li)

        with open(self.sclar_file, 'rb') as file:
            scalar_object = pickle.load(file)
        scalar_object.transform(li)

        lower=(int(prediction[0]))-1000-int(pre)
        upper=(int(prediction[0]))+1000-int(pre)
        return render_template('index.html',prediction_text=str(lower)+' - '+str(upper))

    def run(self):
        self.app.run(debug=False)

  
        


