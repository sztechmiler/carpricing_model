from unittest.mock import inplace
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
import pylab as pl
import numpy as np
import tkinter
import re
import sklearn
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

import seaborn as sns
from scipy.stats import norm

def SetSetting():
    matplotlib.use('TkAgg')
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

def GetMongoDBCollection():
    client = MongoClient()
    carPricingDB = client.carPricing
    firstOffersCollection = carPricingDB.firstOffers
    return firstOffersCollection

def GetZafiryDataFrame(cursor):
    data = pd.DataFrame(list(cursor))
    # zafiry = data[{'Rok produkcji', 'Przebieg', 'Pojemność skokowa', 'Rodzaj paliwa', 'Moc', 'price'}]
    zafiry = data[{'Przebieg', 'price', 'Rok produkcji', 'Moc', 'Rodzaj paliwa'}]
    zafiry.dropna(inplace=True)
    return zafiry

SetSetting()
headerNumber = 20
query_Zafiry = {"Marka pojazdu":'Opel', "Model pojazdu": 'Insignia', "Uszkodzony": { "$exists" : False }}
# query_Zafiry = {"Marka pojazdu":'Opel', "Model pojazdu": 'Zafira', "Uszkodzony": { "$exists" : False }, "price": '7 900        PLN'}
firstOffersCollection = GetMongoDBCollection()
allDataAboutZafiry = firstOffersCollection.find(query_Zafiry)

zafiry = GetZafiryDataFrame(allDataAboutZafiry)

def ChangeValuesToNumbers(columnName):
    emtpyString = ''
    zafiraFeatureColumn = zafiry[columnName]
    newColumnValues = zafiraFeatureColumn.apply(lambda x: float(emtpyString.join(re.findall(r'\d+', x))))
    zafiry.drop(columns=[columnName], inplace=True)
    zafiry[columnName] = newColumnValues.tolist()

ChangeValuesToNumbers('price')
ChangeValuesToNumbers('Przebieg')
# ChangeValuesToNumbers('Pojemność skokowa')
ChangeValuesToNumbers('Moc')
ChangeValuesToNumbers('Rok produkcji')

zafiry['Age'] = 2020 - zafiry['Rok produkcji']
zafiry.drop(columns=['Rok produkcji'], inplace = True)

zafiry = pd.get_dummies(zafiry)
# print(zafiry.columns)
zafiry['plnKmDiv10exp6'] = zafiry['price'] * zafiry['Przebieg'] / 1000000
zafiry.sort_values(by=['plnKmDiv10exp6'], inplace = True, ascending=True)


mean = zafiry['plnKmDiv10exp6'].mean()
std = zafiry['plnKmDiv10exp6'].std()
zafiry = zafiry[(zafiry['plnKmDiv10exp6'] > (mean-1*std)) & (zafiry['plnKmDiv10exp6'] < (mean+2*std))]

cos = np.random.rand(len(zafiry))  < 0.8
zafiry_trainSet = zafiry[cos]
zafiry_testSet = zafiry[~cos]

# regr = linear_model.LinearRegression(fit_intercept =True)
# x = np.asanyarray(zafiry_trainSet[['Przebieg']])
# y = np.asanyarray(zafiry_trainSet[['price']])
# regr.fit (x, y)
#
# a = regr.coef_[0][0]
# b = regr.coef_[0][1]
# d = regr.coef_[0][5]
# c = regr.intercept_
# # wspolczynniki = regr.coef_[0]
# print("..........................................")
#
# print("")
# print(str(regr.coef_))
# print(str(regr.intercept_))
#
# print("..........................................")
#
# millage = 64487
# age = 3
# real_price = 68800
#
# price = a* millage + age * b + c + d
# diff_price = real_price-price
# print("..........................................")
# print("price: " + str(price))
# print("real price: " + str(real_price))
# print("diff in price: " + str(diff_price))
# print("diff in price in % : " + str(diff_price/real_price))




# y_hat = regr.predict(zafiry_testSet[['Przebieg']]) #był Przebieg
# x = np.asanyarray(zafiry_testSet[['Przebieg']])
# # x = np.asanyarray(zafiry_testSet[['Przebieg', 'age', 'Rodzaj paliwa_Benzyna',  'Rodzaj paliwa_Benzyna+CNG','Rodzaj paliwa_Benzyna+LPG',  'Rodzaj paliwa_Diesel']])
# y = np.asanyarray(zafiry_testSet[['price']])
# # print("Residual sum of squares: %.2f" % np.mean((y_hat - y) ** 2))


# Explained variance score: 1 is perfect prediction

# ---------------------------
# write your code here
train_x = np.asanyarray(zafiry_trainSet[['Przebieg', 'Age']])
train_y = np.asanyarray(zafiry_trainSet[['price']])

test_x = np.asanyarray(zafiry_testSet[['Przebieg', 'Age']])
test_y = np.asanyarray(zafiry_testSet[['price']])


poly = PolynomialFeatures(degree=3)
train_x_poly = poly.fit_transform(train_x)
# train_x_poly
print("featureNames: " + str(poly.get_feature_names(['Przebieg', 'Age'])))

clf = linear_model.LinearRegression()
train_y_ = clf.fit(train_x_poly, train_y)
# The coefficients
print ('Coefficients: ', clf.coef_)
print ('Intercept: ',clf.intercept_)

def plotModel():
    plt.scatter(zafiry_trainSet.Przebieg, zafiry_trainSet.price,  color='blue')
    XX = np.arange(0.0, zafiry['Przebieg'].max(),zafiry['Przebieg'].max()/1000)
    yy = clf.intercept_[0]+ clf.coef_[0][1]*XX+ clf.coef_[0][2]*np.power(XX, 2)+clf.coef_[0][3]*np.power(XX, 3)
    plt.plot(XX, yy, '-r' )
    plt.xlabel("Millage")
    plt.ylabel("Price")
    plt.show()

def plot3DModel():
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Make data.
    przebieg = np.arange(0.0, zafiry['Przebieg'].max(),zafiry['Przebieg'].max()/1000)
    age = np.arange(0.0, zafiry['Age'].max(),zafiry['Age'].max()/20)
    przebieg, age = np.meshgrid(przebieg, age)
    # featureNames: ['1', 'Przebieg', 'Age', 'Przebieg^2', 'Przebieg Age', 'Age^2', 'Przebieg^3', 'Przebieg^2 Age', 'Przebieg Age^2', 'Age^3']
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
    # yy = clf.intercept_[0]+ clf.coef_[0][1]*XX+ clf.coef_[0][2]*np.power(XX, 2)+clf.coef_[0][3]*np.power(XX, 3)
    price = intercept + np.power(przebieg, 1) * przebieg_coef + np.power(przebieg, 2) *przebieg2_coef + np.power(przebieg, 3) * przebieg3_coef +\
            np.power(age, 1) * age_coef + np.power(age, 2)* age2_coef + np.power(age,3)*age3_coef +\
            przebieg * age * przebieg_age_coef + np.power(przebieg, 2) * age * przebieg2_age_coef + np.power(age,2) * przebieg * przebieg_age2_coef
    # Plot the surface.
    surf = ax.plot_surface(przebieg, age, price, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(0, 100000)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def plot3DModelRealData():
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Make data.
    przebieg =zafiry['Przebieg']
    age = zafiry['Age']
    price = zafiry['price']
    # Plot the surface.
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(przebieg, age, price, linewidth=0.2, antialiased=True)
    plt.show()



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