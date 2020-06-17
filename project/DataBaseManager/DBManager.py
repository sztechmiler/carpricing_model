from pymongo import MongoClient
import pandas as pd
import re
from CarModel.Cars import Car 
#to run mongodb in terminal run sudo service mongod status

def getValueFromString(strVal):
    x = float(''.join(re.findall(r'\d+', strVal)))
    return x



def get_cars(brand="", model =""):
    if (model==""): 
        carQuery = {"Uszkodzony": { "$exists" : False }}
    else:
        carQuery = {"Marka pojazdu": brand, "Model pojazdu": model, "Uszkodzony": { "$exists" : False }}
    cars = []
    client = MongoClient()
    car_pricing_db = client["carPricing"]
    firstOffersCollection = car_pricing_db.firstOffers
    cos = firstOffersCollection.find(carQuery).limit(50)

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
