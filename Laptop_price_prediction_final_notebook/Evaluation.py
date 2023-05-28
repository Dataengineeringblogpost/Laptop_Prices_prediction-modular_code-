from sklearn.metrics import r2_score,mean_squared_error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
class Evaluation():
    def __init__(self,x_test,y_test,x,y):
        self.x_test=x_test
        self.y_test=y_test
        self.x=x
        self.y=y
        
    def regression(self,model,head_value=5):
        x_test=self.x_test
        y_test=self.y_test
        x=self.x
        y=self.y
        print("---------------------------------------- SCORE ------------------------------------------------")
        print()
        print("The Score of test matrics:- ",model.score(x_test,y_test))
        print()
        print("---------------------------------------- R-Squared, RMSE , Adj R-Square  ------------------------------------------------")
        print()
        Y_PRED=model.predict(x_test)
        r2=r2_score(y_test,Y_PRED)
        print("R-squared:",r2)

        rmse=np.sqrt(mean_squared_error(y_test,Y_PRED))
        print("RMSE:",rmse)
        
        adjusted_r_squared = 1 - (1-r2)*(len(y)-1)/(len(y)-x.shape[1]-1)
        print("Adj R-square:",adjusted_r_squared)
        #Dataframe to have everything in one
        new_df=pd.DataFrame()
        
        new_df['Actual sales']=y_test
        new_df['Predicted sales']=Y_PRED
        new_df['Error']=abs(y_test-Y_PRED)
        
        plt.figure(figsize=(28,12))
        new_df.reset_index(inplace=True)
        new_df['Actual sales'].plot()
        new_df['Predicted sales'].plot()
        plt.xlabel("INDEX")
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        plt.legend()
        return new_df.head(head_value)
    
    def classification(self,model):
        X_test=self.x_test
        Y_test=self.y_test
        print("---------------------------------------- SCORE ------------------------------------------------")
        print()
        print("The Score of test matrics:- ",model.score(X_test,Y_test))
        print()
        print("---------------------------------------- Confusion Matrix , tn , fp , fn , tp ------------------------------------------------")
        print()
        print("Confusion Matrix:-")
        y_pred=model.predict(X_test)
        cfm=confusion_matrix(Y_test,y_pred)
        print(cfm)
        tn, fp, fn, tp = cfm.ravel()
        print()
        print('True Negtive:-',tn,"\nFalse Postive(Type 1 Error)[precision]:-", fp, "\nFalse negtive(Type 2 Error)[Recall]:- ",fn, "\nTrue Postive:-",tp)
        print()
        print('Classification Report:- ')
        print(classification_report(Y_test,y_pred))
        print()
        acc=accuracy_score(Y_test,y_pred)
        print("Accuracy of the model:",acc)
        