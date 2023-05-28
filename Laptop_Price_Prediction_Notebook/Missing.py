import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import missingno as msno
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
class Missing():
    def __init__(self,df):
        self.files=df
    #---------------------------------------------------- Data Cleaning ------------------------------------------------------------------ 
    #Missing:-data cleaning dataframe 
    def missing(self):
        missing=pd.DataFrame(columns=['column name',"datatype","unique","sample_value_of_the_column","Missing values","Missing percentage","category_"])
        data=self.files.dtypes
        
        for itr in range(0,len(self.files.columns)):
            columns_name=self.files.columns[itr]
            datatype=data[itr]
            cat=self.files[columns_name].nunique()
            sample=self.files[columns_name].head(1).values[0]
            nu=self.files[columns_name].isna().sum()
            per=round((self.files[columns_name].isnull().sum()/len(self.files))*100)
            per=str(per)+'%'
            cat1=''
            
            if datatype!='object':
                if cat<10:
                    cat1='Discrete(mode)'
                else:
                    cat1='Continous(mean/median)'
            else:
                cat1='Categorical(mode)'
            

            missing.loc[itr]=[columns_name,datatype,cat,sample,nu,per,cat1]
        missing.sort_values(['Missing values'],ascending=False,inplace=True)
        return missing 
    
    #Graph missing:-Making graph with missing 
    def graph_missing(self):
        sns.displot(height=7,data=self.files.isna().melt(value_name="missing"),y="variable",hue="missing",multiple="fill",aspect=1.25)
    #------------------------------------------------------Fill missing values using Mean,Median,Mode--------------------------------------------------------------

    #outliers with series for checking mean,median
    def outlier(self,ser):
        out=[]
        Q1 = np.percentile(ser, 25,
                interpolation = 'midpoint')

        Q3 = np.percentile(ser, 75,
                        interpolation = 'midpoint')
        IQR = Q3 - Q1

        # Upper bound
        upper = np.where(ser >= (Q3+1.5*IQR))
        # Lower bound
        lower = np.where(ser <= (Q1-1.5*IQR))
        out=np.concatenate((upper,lower),axis=1)
        out=out.tolist()
        if len(out[0])!=0:   
            return 'out'
        else:
            return "No out"
        return outliers_col

    #filling mean,median,mode where ever required
    def fill_mean_mode(self):
        df=self.files
        data=df.dtypes
        col=df.columns
        for itr in range(0,len(df.columns)):
            
            datatype=data[itr]
            col_name=col[itr]
            if df[col_name].isnull().sum()!=0:
                if datatype!='object':
                    if self.outlier(df[col_name])=='out':
                        df[col_name]=df[col_name].fillna(df[col_name].median())
                    else:
                        df[col_name]=df[col_name].fillna(df[col_name].mean())
                else:
                    df[col_name]=df[col_name].fillna(df[col_name].mode()[0])    
        print('Done ✅ ')
        return df.isnull().sum()
    
    #--------------------------------------------------------------Simple imputer -------------------------------------------------------------------
    #--------------------------------------------------------------Model Missing --------------------------------------------------------------------
    def model_missing(self,x,y,model_object):
            x_col=x.columns
            """
            x_:-x df without nan
            y_:-y df without nan
            x_pred:-x df with nan for prediction
            y_pred:-y df with nan for prediction
            """
#             imputer = KNNImputer(n_neighbors=2)
#             x= imputer.fit_transform(x)
            x=pd.DataFrame(x,columns=x_col)
            y_p=y[y.isnull()]
            print(y_p)
            y_=y[~y.isnull()]
            x_pred=x.loc[y_p.index]
            x_=x.loc[y_.index]
            
            
            X_train, X_test,y_train, y_test = train_test_split(x_,y_ ,
                                        random_state=10, 
                                        test_size=0.20)
            model_object.fit(X_train,y_train)
            print("The Score value", model_object.score(X_test,y_test))
            inp=input("If continue press yes")
            if inp=='yes':
                a={}
                model_object.fit(x_,y_)
                y_pred=model_object.predict(x_pred)
                y_pred=pd.Series(y_pred)
                x_frames = [x_,x_pred]
                x = pd.concat(x_frames)
                x=x.sort_index(axis = 0)
                y_frames=[y_,y_pred]
                y =  pd.concat(y_frames)
                y=y.sort_index(axis = 0)
                a['x']=x
                a['y']=y
                return a
            else:
                return "no"    