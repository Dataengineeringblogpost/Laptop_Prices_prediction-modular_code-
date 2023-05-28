


def model_space():
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    from xgboost import XGBRegressor
    from sklearn.ensemble import AdaBoostRegressor
    from sklearn.linear_model import SGDRegressor
    from sklearn.svm import SVR
    models = {
        'RandomForestClassifier': {
            'model': RandomForestRegressor(),
            'params': {'n_estimators': [10, 50, 100],
                        'max_depth': [2, 5, 10]}
        },
        
        'KNeighborsRegressor': {
            'model': KNeighborsRegressor(),
            'params':{'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance']}
    },
    
    
       }
    return models
   