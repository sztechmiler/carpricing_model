from pymongo import MongoClient
import pandas as pd
import re
from datetime import datetime

from CarModel.Cars import Car 
#to run mongodb in terminal run sudo service mongod status

def getValueFromString(strVal):
    x = float(''.join(re.findall(r'\d+', strVal)))
    return x



def get_cars(brand="", model="", limit=0):
    if (model==""): 
        carQuery = {"Uszkodzony": { "$exists" : False }}
    else:
        carQuery = {"Marka pojazdu": brand, "Model pojazdu": model, "Uszkodzony": { "$exists" : False }}
    cars = []
    client = MongoClient()
    car_pricing_db = client["carPricing"]
    firstOffersCollection = car_pricing_db.firstOffers
    cos = firstOffersCollection.find(carQuery).limit(limit)

    data = pd.DataFrame(list(cos))
    # price, brand, model, fuel, millage, year, gearBox, capacity, power, features, drive):
    data = data[{'price', 'Marka pojazdu','Model pojazdu', 'Rodzaj paliwa', 'Przebieg',
                    'Rok produkcji','Skrzynia biegów','Pojemność skokowa', 'Moc', 'Napęd'}]
    data = data.dropna()
    for index, row in data.iterrows():
        carDict = {
        "price": getValueFromString(row['price']),
        "brand": row['Marka pojazdu'],
        "model": row['Model pojazdu'],
        "fuel": row['Rodzaj paliwa'],
        "millage": getValueFromString(row['Przebieg']),
        "year": row['Rok produkcji'],
        "gearBox": row['Skrzynia biegów'],
        "capacity": getValueFromString(row['Pojemność skokowa']),
        "power": getValueFromString(row['Moc']),
        "drive": row['Napęd']
        }

        car = Car(**carDict)
        cars.append(car)
    return cars

def insert_db_pricing_model_poly3_allfeatures(brand, model, model_parameters):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    client = MongoClient()
    car_pricing_db = client.carPricing
    features_collection = car_pricing_db.features
    features_collection.insert_one(
    {"brand": brand,
     "model": model,
     "poly": 3,
     "level_of_details": "high",
     "update_time": now,
     "model_factors": model_parameters})

def get_unique_brands_with_model():
    client = MongoClient()
    car_pricing_db = client["carPricing"]
    features_collection = car_pricing_db.features
    unique_brands = features_collection.distinct(key='brand')
    return unique_brands

def get_unique_models_with_model(brand):
    client = MongoClient()
    car_pricing_db = client["carPricing"]
    features_collection = car_pricing_db.features
    query = {"brand": brand}

    unique_models = features_collection.distinct(key='model', query=query)
    return unique_models


def get_unique_brands():
    client = MongoClient()
    car_pricing_db = client["carPricing"]
    firstOffersCollection = car_pricing_db.firstOffers
    unique_brands = firstOffersCollection.distinct(key='Marka pojazdu')
    return unique_brands

def get_unique_modles(brand):
    client = MongoClient()
    car_pricing_db = client["carPricing"]
    firstOffersCollection = car_pricing_db.firstOffers
    query = {"Marka pojazdu": brand}

    unique_models = firstOffersCollection.distinct(key='Model pojazdu', query=query)
    return unique_models
