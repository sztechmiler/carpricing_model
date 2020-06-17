#bin/python3
# from .. import CarModel
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import sklearn



class PricingModel:
    def __init__(self, cars):
        self.cars = cars #this is to be a list of cars e.g. Zafiras

    def excludeStrangeUnites(self, df):
        df['plnKmDiv10exp6'] = df['price'] * df['millage'] / 1000000
        df.sort_values(by=['plnKmDiv10exp6'], inplace = True, ascending=True)
        mean = df['plnKmDiv10exp6'].mean()
        std = df['plnKmDiv10exp6'].std()

        return df[(df['plnKmDiv10exp6'] > (mean-1*std)) & (df['plnKmDiv10exp6'] < (mean+2*std))]  #we exclude strange millage vs price 


    def getModelParameters(self):
        list_of_cars =  [Car.carDict for Car in self.cars] #get list of dictionaries from cars i.e. for car in cars get cars.dict and put in into the list ...
        data = pd.DataFrame(list_of_cars) #should change to DataFrame
        data.drop(columns=['brand', 'model'], inplace=True)

        data = pd.get_dummies(data)     #should get dummies i.e. manual_gearbox = 1, automat_gearbox = 0
        data = self.excludeStrangeUnites(data)

        train_indexes = np.random.rand(len(data))  < 0.8
        data_trainSet = data[train_indexes]
        data_testSet = data[~train_indexes]

        #* here we start to build model ;-)
        #? set x and y of train and test (populations)
        data_train_set_x = data_trainSet.drop(columns=['price'], inplace=False)
        data_train_set_y = data_trainSet[['price']]
        data_test_set_x = data_testSet.drop(columns=['price'], inplace=False)
        data_test_set_y = data_testSet[['price']]
        # print(data_train_set_x.columns)
        # print(data_train_set_x.head(10))

        
        poly_degree = 3
        result_dict = {"intercept": 0}
        for feature in data_test_set_x.columns:    
            for i in range(poly_degree):
                result_dict[feature + '_' + str(i+1)] = 0



        train_x = np.asanyarray(data_train_set_x) 
        train_y = np.asanyarray(data_train_set_y)            
        test_x = np.asanyarray(data_test_set_x) 
        test_y = np.asanyarray(data_test_set_y)
        
        #? set 3 degree polinomial -> simply we change train_x to have age, age^2, age^3, millage, millage^2, millage^3 (simpler then you think ;-)  
        poly = PolynomialFeatures(degree=poly_degree)
        train_x_poly = poly.fit_transform(train_x)

        
        clf = linear_model.LinearRegression()
        train_y_ = clf.fit(train_x_poly, train_y) #! here we need to cahnge a bit ;-) 
        # The coefficients
        # print ('Coefficients: ', clf.coef_)
        # print ('Intercept: ',clf.intercept_)
        intercept = clf.intercept_.tolist()[0]
        factors = clf.coef_.tolist()[0]
        index = 0
        for k, v in result_dict.items():
            if(k == "intercept"):
                result_dict[k] = intercept
            else:
                result_dict[k] = factors[index]
                index += 1

        result = clf.intercept_.tolist()
        result = result + clf.coef_.tolist()[0]
        print(result_dict)
        return result_dict

        test_x_poly = poly.fit_transform(test_x)
        predicted_test_y = clf.predict(test_x_poly)

        meanAbsoluteError = sklearn.metrics.mean_absolute_error(test_y, predicted_test_y)
        print("Mean absolute error: %.2f" % meanAbsoluteError)
        r2Score = sklearn.metrics.r2_score(test_y, predicted_test_y)
        print("R2-score: %.2f" % r2Score )
        meanSquareError = sklearn.metrics.mean_squared_error(test_y, predicted_test_y)
        print("Mean squared error: %.2f" % meanSquareError)
        errorAsPercentOfRealPrice = test_y.mean() / meanAbsoluteError;
        print("In general each price is different by around: %.2f" % errorAsPercentOfRealPrice + "%")
        # print p.get_feature_names(data.columns)
        # plotModel()
        # plot3DModel()
        # plot3DModelRealData()
        przebieg = 120200
        age = 4

        intercept = clf.intercept_[0]
        przebieg_coef = clf.coef_[0][1]
        age_coef = clf.coef_[0][2]
        przebieg2_coef = clf.coef_[0][3]
        przebieg_age_coef = clf.coef_[0][4]
        age2_coef = clf.coef_[0][5]
        przebieg3_coef = clf.coef_[0][6]
        przebieg2_age_coef = clf.coef_[0][7]
        przebieg_age2_coef = clf.coef_[0][8]
        age3_coef = clf.coef_[0][9]


        price = intercept + np.power(przebieg, 1) * przebieg_coef + np.power(przebieg, 2) *przebieg2_coef + np.power(przebieg, 3) * przebieg3_coef +\
                    np.power(age, 1) * age_coef + np.power(age, 2)* age2_coef + np.power(age,3)*age3_coef +\
                    przebieg * age * przebieg_age_coef + np.power(przebieg, 2) * age * przebieg2_age_coef + np.power(age,2) * przebieg * przebieg_age2_coef

        print("cena to: " + str(price))


        
