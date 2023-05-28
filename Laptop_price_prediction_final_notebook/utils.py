import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
class utils:
    def __init__(self,files):
        self.files=files
#----------------------------------Describing the data -------------------------------------------
    #basics
    def basics(self):
        #Warnings
        import warnings
        warnings.filterwarnings('ignore')
        #display max columns
        pd.set_option("display.max_columns", None)
        #Get shape
        df=self.files.shape
        print("Shape of the Dataframe:- ")
        print()
        print("Rows:- ",df[0])
        print("Columns:- ",df[1])
        print()
        print('________________________________________________________________________________________________________')
        print()
        print('Columns of the Dataframe:-')
        print()
        print("columns:-",self.files.columns)
        
    #Datatypes 
    def datatypes_data(self):
        pd.set_option("display.max_columns", None)
        # pd.set_option("display.max_rows", None)
        data=self.files.dtypes
        dtype_df=pd.DataFrame(columns=['Column_Name',"datatype","unique","sample_value_of_the_column","Number_of_missing_value_present"])
        for itr in range(0,len(self.files.columns)):
            columns_name=self.files.columns[itr]
            datatype=data[itr]
            cat=self.files[columns_name].nunique()
            sample=self.files[columns_name].head(1).values[0]
            nu=self.files[columns_name].isna().sum()

            dtype_df.loc[itr]=[columns_name,datatype,cat,sample,nu]
        return dtype_df
#---------------------------------------------------- Data Cleaning ------------------------------------------------------------------ 
    #missing 
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
    
    #outliers with series
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
    
    #Checking wheather dataframe  is totally clean or not
    def check_missing(self):
        df=self.files
        df_col=[]
        col=df.columns
        for itr in range(0,len(df.columns)):
            col_name=col[itr]
            if df[col_name].isnull().sum()!=0:
                df_col.append(col_name)
        if len(df_col)!=0:
            print(df_col)
            return "missing value present"
        else:
            return "No Missing value present"
#-----------------------------------------------------------------Outlier handling ----------------------------------------------------
    #Get outlier columns
    def get_outlier_col(self):
        df=self.files
        num=df.select_dtypes(exclude='object')
        outliers_col=[]
        for col_name in num.columns:
            out=[]
            
            Q1 = np.percentile(df[col_name], 25,
                    interpolation = 'midpoint')
    
            Q3 = np.percentile(df[col_name], 75,
                            interpolation = 'midpoint')
            IQR = Q3 - Q1

            # Upper bound
            upper = np.where(df[col_name] >= (Q3+1.5*IQR))
            # Lower bound
            lower = np.where(df[col_name] <= (Q1-1.5*IQR))
            out=np.concatenate((upper,lower),axis=1)
            out=out.tolist()
            if len(out[0])!=0:
                outliers_col.append(col_name)
                print(col_name)
                print( "Outliers:- " ,str(len(out[0])))
            else:
                print(col_name)
                print("No Outliers")
        return outliers_col
    #Box plot for outliers
    def out_vis(self,outlier_col):
        df=self.files
        
        len_outlier_col=len(outlier_col)
        col=round(len_outlier_col/2)
        
        fig, axes = plt.subplots( col,2,figsize=(col*1.5,col*7))
        i=0
        j=0


        for itr in outlier_col:
            sns.boxplot(df[itr],ax=axes[j,i])
        
            axes[j,i].tick_params(axis="x", labelsize=27) 

        
            axes[j,i].set_xlabel(itr, fontsize = 27)
    #         axes[j,i].set_linewidth(2.5)
            if i==1:
                j+=1
                i=0
            else:
                i=i+1
    #     mpl.rcParams['axes.linewidth'] = 0.1 #set
        fig.tight_layout(pad=3.0)
        plt.show()

